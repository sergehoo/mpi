from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Pas de redirection HTTPS
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False