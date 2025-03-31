from rest_framework import serializers

from patient.models import Platform, Patient


class PlatformSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les plateformes connectées au MPI
    """

    class Meta:
        model = Platform
        fields = ['id', 'name', 'api_key', 'is_active']


class PatientSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les patients
    """
    platforms_registered = PlatformSerializer(many=True, read_only=True)
    platforms_accessed = PlatformSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = [
            'upi', 'code_patient', 'code_vih', 'nom', 'prenoms', 'contact',
            'adresse_mail', 'date_naissance', 'genre', 'nationalite', 'ethnie',
            'profession', 'employeur', 'niveau_etude', 'groupe_sanguin',
            'cmu', 'urgence', 'created_at', 'updated_at', 'qr_code',
            'platforms_registered', 'platforms_accessed'
        ]
        read_only_fields = ['upi', 'created_at', 'updated_at', 'platforms_registered', 'platforms_accessed']
