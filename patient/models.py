import datetime
import io
import uuid

from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_L
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models, transaction
# import qrcode
from django.db.models import Max
from django.utils.crypto import get_random_string

from patient.utils import nettoyer_numero_international


def generate_api_key():
    return get_random_string(length=40)


class Platform(models.Model):
    """
    Représente une plateforme (ex: Laboratoire, Surveillance, Hospitalisation)
    """
    name = models.CharField(max_length=255, unique=True)
    api_key = models.CharField(max_length=255, default=generate_api_key, unique=True)  # Clé d'authentification unique
    is_active = models.BooleanField(default=True)  # Permet de verrouiller l'accès à une plateforme
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Utilisateur associé
    webhook_url = models.URLField(null=True, blank=True, help_text="URL de notification de la plateforme")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    """
    Modèle Patient unique à travers les plateformes
    """
    upi = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)  # Identifiant global MPI
    # Informations personnelles
    nom = models.CharField(max_length=225, db_index=True)
    prenoms = models.CharField(max_length=225, db_index=True)
    date_naissance = models.DateField(db_index=True)
    contact = models.CharField(max_length=225, db_index=True)
    contact_pays = models.CharField(max_length=200, blank=True, null=True, help_text="Code ISO pays (ex: CI, FR)")
    contact_second = models.CharField(max_length=225, db_index=True)
    adresse_mail = models.EmailField(max_length=50, blank=True, unique=True, null=True)
    sexe = models.CharField(max_length=20, null=True, blank=True)
    nationalite = models.CharField(max_length=200, null=True, blank=True)
    ethnie = models.CharField(null=True, blank=True, max_length=100)
    # Informations professionnelles
    profession = models.CharField(max_length=100, null=True, blank=True)
    employeur = models.CharField(max_length=100, null=True, blank=True)
    niveau_etude = models.CharField(max_length=100, null=True, blank=True)
    # Informations médicales
    groupe_sanguin = models.CharField(
        choices=[('A+', 'A+'), ('O+', 'O+'), ('B+', 'B+'), ('AB+', 'AB+'), ('A-', 'A-'), ('O-', 'O-'), ('B-', 'B-'),
                 ('AB-', 'AB-')],
        max_length=20, null=True, blank=True
    )
    num_cmu = models.CharField(max_length=100, null=True, blank=True,db_index=True)
    cni_num = models.CharField(max_length=100, null=True, blank=True,db_index=True)
    cni_nni = models.CharField(max_length=100, null=True, blank=True,db_index=True)

    pere = models.ForeignKey('self', on_delete=models.CASCADE, related_name="parent_pere", null=True, blank=True)
    mere = models.ForeignKey('self', on_delete=models.CASCADE, related_name="parent_mere", null=True, blank=True)

    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    updated_at = models.DateTimeField(auto_now=True,db_index=True)

    # Liens avec les plateformes
    platforms_registered = models.ManyToManyField(Platform, related_name="patients_registered", blank=True)
    platforms_accessed = models.ManyToManyField(Platform, related_name="patients_accessed", blank=True)

    # QR Code
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        permissions = (
            ('view_patient_name', 'Can view patient name'),
            ('view_dossier_patient', 'Can View dossier patient'),
        )

    def clean_contact(self):
        pays = self.contact_pays or 'CI'
        numero_nettoye = nettoyer_numero_international(self.contact, pays)
        if not numero_nettoye:
            raise ValidationError("Numéro de téléphone invalide pour ce pays.")
        self.contact = numero_nettoye

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.generate_qr_code()
        self.clean_contact()
        super(Patient, self).save(*args, **kwargs)

    def generate_qr_code(self):
        qr = QRCode(
            version=1,
            error_correction=ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_data = f"Nom: {self.nom} {self.prenoms}\nContact: {self.contact}\nUPI: {self.upi}"
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        file_name = f"qr_code_{self.upi}.png"

        self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)

    def __str__(self):
        return f'{self.prenoms} {self.nom} - {self.upi}'


class PatientHistorique(models.Model):
    """
    Stocke l'historique des informations évolutives du patient
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="historique",db_index=True)
    date_debut = models.DateField()  # Date à laquelle cette information est devenue valide
    date_fin = models.DateField(null=True, blank=True)  # Si NULL, cela signifie que c'est encore actuel

    # Évolutif
    adresse = models.TextField(null=True, blank=True,db_index=True)
    contact = models.CharField(max_length=225, null=True, blank=True,db_index=True)
    profession = models.CharField(max_length=100, null=True, blank=True,db_index=True)
    employeur = models.CharField(max_length=100, null=True, blank=True,db_index=True)
    situation_matrimoniale = models.CharField(
        max_length=50,
        choices=[('Célibataire', 'Célibataire'), ('Marié', 'Marié'), ('Divorcé', 'Divorcé'), ('Veuf', 'Veuf')],
        null=True, blank=True
    )
    nbr_enfants = models.PositiveIntegerField(default=0, null=True, blank=True)

    # Santé et assurance

    maladie_chronique = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.patient.nom} {self.patient.prenoms} - {self.date_debut} à {self.date_fin or 'Présent'}"

    class Meta:
        ordering = ['-date_debut']


class PlatformAccessLog(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, db_index=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True,db_index=True)
    action = models.CharField(max_length=50,db_index=True)  # ex: "read", "create", "update"
    date = models.DateTimeField(auto_now_add=True,db_index=True)
    ip = models.GenericIPAddressField(null=True, blank=True,db_index=True)
