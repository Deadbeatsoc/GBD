# auth_backend.py
from django.contrib.auth.backends import BaseBackend
from rutinas.models import Usuario
from django.contrib.auth.hashers import check_password

