import hashlib

import requests
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from patient.apis.serializers import PlatformSerializer, PatientSerializer, PlatformAuthSerializer
from patient.models import Patient, Platform, PlatformAccessLog
from django.db import transaction

from patient.utils import nettoyer_numero_international
from patient.webhook import notifier_plateforme_webhook


# class PlatformTokenView(GenericAPIView):
#     """
#     Permet aux plateformes d'obtenir un token JWT en utilisant leur `api_key` et `username`
#     """
#     serializer_class = PlatformAuthSerializer  # OBLIGATOIRE pour Swagger
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]
#         refresh = RefreshToken.for_user(user)
#
#         return Response({
#             "access": str(refresh.access_token),
#             "refresh": str(refresh)
#         }, status=status.HTTP_200_OK)

class PlatformTokenView(GenericAPIView):
    serializer_class = PlatformAuthSerializer
    permission_classes = [AllowAny]  # 🔥 autorise explicitement accès public

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)


@receiver(post_save, sender=Platform)
def assign_user(sender, instance, created, **kwargs):
    if created and not instance.user:
        user = User.objects.create_user(username=instance.name.lower())
        instance.user = user
        instance.save()


def generate_patient_signature(nom, prenoms, date_naissance):
    base = f"{nom.strip().lower()}_{prenoms.strip().lower()}_{date_naissance}"
    return hashlib.sha256(base.encode()).hexdigest()


def notifier_plateforme_webhook(platform, event, patient_data):
    if platform.webhook_url:
        try:
            requests.post(platform.webhook_url, json={
                "event": event,
                "upi": patient_data.get('upi'),
                "data": patient_data
            }, timeout=5)
        except requests.RequestException:
            pass


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key='ip', rate='10/m', method='GET', block=True))
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        required_fields = ['nom', 'prenoms', 'date_naissance', 'contact']
        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            return Response({"error": f"Champs obligatoires manquants: {', '.join(missing_fields)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        try:
            platform = Platform.objects.get(user=user, is_active=True)
        except Platform.DoesNotExist:
            return Response({"error": "Plateforme non reconnue ou désactivée"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['contact'] = nettoyer_numero_international(data.get('contact'))

        with transaction.atomic():
            existing_patient = None

            # Priorité aux identifiants uniques
            cni_num = data.get('cni_num')
            cni_nni = data.get('cni_nni')
            num_cmu = data.get('num_cmu')

            if cni_num:
                existing_patient = Patient.objects.select_for_update().filter(cni_num=cni_num).first()
            if not existing_patient and cni_nni:
                existing_patient = Patient.objects.select_for_update().filter(cni_nni=cni_nni).first()
            if not existing_patient and num_cmu:
                existing_patient = Patient.objects.select_for_update().filter(num_cmu=num_cmu).first()

            # Fallback si aucun identifiant unique n'est fourni
            if not existing_patient:
                nom = data.get('nom')
                prenoms = data.get('prenoms')
                date_naissance = data.get('date_naissance')
                existing_patient = Patient.objects.select_for_update().filter(
                    nom=nom, prenoms=prenoms, date_naissance=date_naissance
                ).first()

            if existing_patient:
                updated = False
                for field, value in data.items():
                    if value and getattr(existing_patient, field, None) != value:
                        setattr(existing_patient, field, value)
                        updated = True

                if updated:
                    existing_patient.updated_at = timezone.now()
                    existing_patient.save()

                existing_patient.platforms_accessed.add(platform)

                PlatformAccessLog.objects.create(
                    platform=platform,
                    patient=existing_patient,
                    action="update",
                    ip=request.META.get('REMOTE_ADDR')
                )

                notifier_plateforme_webhook(platform, "update", PatientSerializer(existing_patient).data)

                return Response({
                    "message": "Patient existant mis à jour",
                    "upi": existing_patient.upi,
                    "data": PatientSerializer(existing_patient).data
                }, status=status.HTTP_200_OK)

            # Création du nouveau patient
            new_patient = Patient.objects.create(**data)
            new_patient.platforms_registered.add(platform)

            PlatformAccessLog.objects.create(
                platform=platform,
                patient=new_patient,
                action="create",
                ip=request.META.get('REMOTE_ADDR')
            )

            notifier_plateforme_webhook(platform, "create", PatientSerializer(new_patient).data)

            return Response({
                "message": "Nouveau patient enregistré",
                "upi": new_patient.upi,
                "data": PatientSerializer(new_patient).data
            }, status=status.HTTP_201_CREATED)


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer

    @action(detail=True, methods=['post'])
    def toggle_access(self, request, pk=None):
        platform = self.get_object()
        platform.is_active = not platform.is_active
        platform.save()
        return Response({"message": f"Accès {'activé' if platform.is_active else 'désactivé'}"})
