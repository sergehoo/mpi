from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from mpi.api.serializers import PlatformSerializer, PatientSerializer
from patient.models import Patient, Platform
from django.db import transaction


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        - Vérifie si un patient existe déjà sur le MPI
        - Met à jour ses informations si nécessaire
        - Ajoute la plateforme comme ayant accédé au patient
        """
        platform_name = request.headers.get('Platform-Name')  # Récupération de la plateforme
        try:
            platform = Platform.objects.get(name=platform_name, is_active=True)
        except Platform.DoesNotExist:
            return Response({"error": "Plateforme inconnue ou désactivée"}, status=status.HTTP_403_FORBIDDEN)

        # Extraction des données du patient
        nom = request.data.get('nom')
        prenoms = request.data.get('prenoms')
        date_naissance = request.data.get('date_naissance')
        contact = request.data.get('contact')

        # Recherche d'un patient existant via UPI ou informations uniques
        existing_patient = Patient.objects.filter(nom=nom, prenoms=prenoms, date_naissance=date_naissance).first()

        with transaction.atomic():
            if existing_patient:
                # Mise à jour des informations du patient si de nouvelles données sont fournies
                updated = False
                for field, value in request.data.items():
                    if value and getattr(existing_patient, field, None) != value:
                        setattr(existing_patient, field, value)
                        updated = True

                if updated:
                    existing_patient.updated_at = timezone.now()
                    existing_patient.save()

                # Ajout de la plateforme qui a accédé aux données
                existing_patient.platforms_accessed.add(platform)

                return Response(
                    {
                        "message": "Patient existant mis à jour",
                        "upi": existing_patient.upi,
                        "data": PatientSerializer(existing_patient).data
                    },
                    status=status.HTTP_200_OK
                )

            # Si le patient n'existe pas, on le crée
            new_patient = Patient.objects.create(**request.data)
            new_patient.platforms_registered.add(platform)

            return Response(
                {
                    "message": "Nouveau patient enregistré",
                    "upi": new_patient.upi,
                    "data": PatientSerializer(new_patient).data
                },
                status=status.HTTP_201_CREATED
            )

    @action(detail=True, methods=['get'])
    def track_platforms(self, request, pk=None):
        """
        Retourne les plateformes ayant enregistré ou accédé au patient
        """
        patient = self.get_object()
        return Response({
            "platforms_registered": [p.name for p in patient.platforms_registered.all()],
            "platforms_accessed": [p.name for p in patient.platforms_accessed.all()],
        })


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer

    @action(detail=True, methods=['post'])
    def toggle_access(self, request, pk=None):
        """
        Active ou désactive une plateforme
        """
        platform = self.get_object()
        platform.is_active = not platform.is_active
        platform.save()
        return Response({"message": f"Accès {'activé' if platform.is_active else 'désactivé'}"})