# auth_backend.py
from django.contrib.auth.backends import BaseBackend
from rutinas.models import Usuario
from django.contrib.auth.hashers import check_password

class UsuarioBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            # Intentar obtener al usuario por su email
            user = Usuario.objects.get(email=email)
            # Verificar la contraseña usando `check_password` si está encriptada
            if check_password(password, user.contrasena):
                return user
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
