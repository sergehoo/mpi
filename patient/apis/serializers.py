from django.contrib.auth.models import User
from rest_framework import serializers
from patient.models import Platform, Patient


class PlatformAuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    api_key = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
            platform = Platform.objects.get(user=user, api_key=data['api_key'], is_active=True)
        except (User.DoesNotExist, Platform.DoesNotExist):
            raise serializers.ValidationError("Authentification échouée : utilisateur ou clé invalide.")

        data['user'] = user
        return data


class PlatformSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les plateformes connectées au MPI
    """

    class Meta:
        model = Platform
        fields = ['id', 'name', 'api_key', 'is_active']


class PatientSerializer(serializers.ModelSerializer):
    platforms_registered = PlatformSerializer(many=True, read_only=True)
    platforms_accessed = PlatformSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = [
            'upi', 'nom', 'prenoms', 'contact', 'adresse_mail', 'date_naissance', 'sexe',
            'nationalite', 'ethnie', 'profession', 'employeur', 'niveau_etude',
            'groupe_sanguin', 'num_cmu', 'cni_num', 'cni_nni',
            'created_at', 'updated_at', 'qr_code',
            'platforms_registered', 'platforms_accessed'
        ]
        read_only_fields = [
            'upi', 'created_at', 'updated_at', 'platforms_registered', 'platforms_accessed'
        ]
