from django import forms
from Mycoach.models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'contrasena', 'rol', 'edad', 'sexo', 'peso', 'altura', 'fecha_nacimiento']
