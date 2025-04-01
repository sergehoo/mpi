// Fonction pour gérer la soumission du formulaire de contact
function handleContactForm() {
    const contactForm = document.getElementById('contactForm');

    if (contactForm) {
        contactForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            // Récupérer les éléments du DOM
            const submitButton = this.querySelector('button[type="submit"]');
            const submitText = document.getElementById('submitText');
            const submitSpinner = document.getElementById('submitSpinner');
            const formData = new FormData(this);

            // Valider les champs avant envoi
            if (!validateForm(formData)) {
                return;
            }

            // Changer l'état du bouton pendant l'envoi
            submitButton.disabled = true;
            submitText.textContent = 'Envoi en cours...';
            submitSpinner.classList.remove('d-none');

            try {
                // Envoyer les données via AJAX
                const response = await fetch(this.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                    }
                });

                const result = await response.json();

                if (response.ok) {
                    // Succès - afficher un message et réinitialiser le formulaire
                    showAlert('success', 'Merci ! Votre message a été envoyé avec succès.');
                    this.reset();
                } else {
                    // Erreur serveur
                    const errorMsg = result.message || 'Une erreur est survenue lors de l\'envoi.';
                    showAlert('danger', errorMsg);
                }
            } catch (error) {
                // Erreur réseau
                console.error('Erreur:', error);
                showAlert('danger', 'Erreur de connexion. Veuillez réessayer plus tard.');
            } finally {
                // Réinitialiser le bouton
                submitButton.disabled = false;
                submitText.textContent = 'Envoyer la demande';
                submitSpinner.classList.add('d-none');
            }
        });
    }

    // Fonction de validation des champs
    function validateForm(formData) {
        let isValid = true;

        // Valider l'email
        const email = formData.get('email');
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            showFieldError('email', 'Veuillez entrer une adresse email valide.');
            isValid = false;
        } else {
            clearFieldError('email');
        }

        // Valider le téléphone si rempli
        const phone = formData.get('phone');
        if (phone && !/^[\d\s+\-().]{10,20}$/.test(phone)) {
            showFieldError('phone', 'Veuillez entrer un numéro de téléphone valide.');
            isValid = false;
        } else {
            clearFieldError('phone');
        }

        // Valider les champs requis
        const requiredFields = ['name', 'institution', 'message'];
        requiredFields.forEach(field => {
            if (!formData.get(field)?.trim()) {
                showFieldError(field, 'Ce champ est obligatoire.');
                isValid = false;
            } else {
                clearFieldError(field);
            }
        });

        return isValid;
    }

    // Afficher une erreur pour un champ spécifique
    function showFieldError(fieldId, message) {
        const field = document.getElementById(fieldId);
        if (!field) return;

        // Créer ou mettre à jour le message d'erreur
        let errorElement = field.nextElementSibling;
        if (!errorElement || !errorElement.classList.contains('invalid-feedback')) {
            errorElement = document.createElement('div');
            errorElement.className = 'invalid-feedback';
            field.parentNode.insertBefore(errorElement, field.nextSibling);
        }

        errorElement.textContent = message;
        field.classList.add('is-invalid');
    }

    // Effacer l'erreur d'un champ
    function clearFieldError(fieldId) {
        const field = document.getElementById(fieldId);
        if (!field) return;

        field.classList.remove('is-invalid');
        const errorElement = field.nextElementSibling;
        if (errorElement && errorElement.classList.contains('invalid-feedback')) {
            errorElement.textContent = '';
        }
    }

    // Afficher une alerte globale
    function showAlert(type, message) {
        // Supprimer les alertes existantes
        const existingAlerts = document.querySelectorAll('.form-alert');
        existingAlerts.forEach(alert => alert.remove());

        // Créer la nouvelle alerte
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} form-alert alert-dismissible fade show mt-3`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        // Insérer après le formulaire
        contactForm.parentNode.insertBefore(alertDiv, contactForm.nextSibling);

        // Fermer automatiquement après 5 secondes
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
}

// Initialiser le gestionnaire de formulaire lorsque le DOM est chargé
document.addEventListener('DOMContentLoaded', function () {
    handleContactForm();

    // Ajouter des styles CSS pour les erreurs de validation si nécessaire
    if (!document.getElementById('form-validation-styles')) {
        const style = document.createElement('style');
        style.id = 'form-validation-styles';
        style.textContent = `
            .is-invalid {
                border-color: #dc3545 !important;
                background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' width='12' height='12' fill='none' stroke='%23dc3545'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23dc3545' stroke='none'/%3e%3c/svg%3e");
                background-repeat: no-repeat;
                background-position: right calc(0.375em + 0.1875rem) center;
                background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
            }
            .is-invalid:focus {
                box-shadow: 0 0 0 0.25rem rgba(220, 53, 69, 0.25);
            }
            .invalid-feedback {
                display: block;
                width: 100%;
                margin-top: 0.25rem;
                font-size: 0.875em;
                color: #dc3545;
            }
        `;
        document.head.appendChild(style);
    }
});