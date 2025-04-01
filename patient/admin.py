from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from patient.models import Platform, Patient, PatientHistorique, ContactMessage


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_active', 'show_api_key', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'user__username', 'api_key')
    readonly_fields = ('api_key', 'show_api_key')  # Mettre show_api_key ici pour éviter l'erreur
    ordering = ('-created_at',)

    def show_api_key(self, obj):
        """Affiche la clé API en lecture seule avec protection"""
        return mark_safe(f'<span style="font-weight: bold; color: red;">{obj.api_key}</span>')

    show_api_key.short_description = "API Key"

    fieldsets = (
        ("Informations Générales", {
            "fields": ("name", "user", "is_active")
        }),
        ("Authentification", {
            "fields": ("api_key", "show_api_key")  # Correction ici
        }),
    )


# @admin.register(Patient)
# class PatientAdmin(admin.ModelAdmin):
#     list_display = (
#         'nom', 'prenoms', 'date_naissance', 'contact', 'profession', 'created_at')
#     list_filter = ('profession', 'groupe_sanguin', 'nationalite')
#     search_fields = ('nom', 'prenoms', 'contact', 'adresse_mail')
#     readonly_fields = ('upi', 'qr_code', 'created_at', 'updated_at')
#
#     fieldsets = (
#         ("Informations Personnelles", {
#             "fields": ("nom", "prenoms", "date_naissance", "genre", "nationalite", "ethnie")
#         }),
#         ("Coordonnées", {
#             "fields": ("contact", "adresse_mail")
#         }),
#         ("Profession", {
#             "fields": ("profession", "employeur", "niveau_etude")
#         }),
#         ("Données Médicales", {
#             "fields": ("groupe_sanguin", "cmu", "urgence")
#         }),
#         ("Données Système", {
#             "fields": ("upi", "qr_code", "created_at", "updated_at")
#         })
#     )
#
#     def get_readonly_fields(self, request, obj=None):
#         if obj:
#             return self.readonly_fields + ('nom', 'prenoms', 'date_naissance')
#         return self.readonly_fields
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenoms', 'date_naissance', 'contact', 'show_platforms_accessed')
    list_filter = ('profession', 'nationalite')
    search_fields = ('nom', 'prenoms', 'contact', 'adresse_mail')
    readonly_fields = ('upi', 'created_at', 'updated_at', 'platforms_registered', 'platforms_accessed')

    def show_platforms_accessed(self, obj):
        """Affiche les plateformes ayant accédé au patient"""
        platforms = ", ".join([p.name for p in obj.platforms_accessed.all()])
        return platforms if platforms else "Aucune"

    show_platforms_accessed.short_description = "Plateformes ayant accédé"


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'is_active', 'is_staff', 'date_joined')
#     list_filter = ('is_staff', 'is_active')
#     search_fields = ('username', 'email')

@admin.register(PatientHistorique)
class PatientHistoriqueAdmin(admin.ModelAdmin):
    list_display = (
    'patient', 'date_debut', 'date_fin', 'adresse', 'contact', 'profession', 'employeur', 'situation_matrimoniale')
    search_fields = ('patient__nom', 'patient__prenoms', 'adresse', 'contact', 'profession')
    ordering = ['-date_debut']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'institution', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'institution', 'message')
    readonly_fields = ('name', 'email', 'institution', 'phone', 'message', 'created_at')

    def has_add_permission(self, request):
        return False  # on empêche la création depuis l'admin
