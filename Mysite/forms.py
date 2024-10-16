from django import forms
from django.contrib.auth.hashers import make_password

from rutinas.models import Usuario  # Para encriptar la contraseña


class UsuarioForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput)

class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'contrasena', 'rol', 'edad', 'sexo', 'peso', 'altura', 'fecha_nacimiento']

def clean_contrasena(self):
        # Encripta la contraseña antes de guardarla en la base de datos
        contrasena = self.cleaned_data.get('contrasena')
        return make_password(contrasena)


class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo Electrónico")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")



    