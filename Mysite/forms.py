from django import forms
from django.contrib.auth.hashers import make_password

from rutinas.models import Ejercicio, Nutricion, Usuario  # Para encriptar la contraseña


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


class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['nombre_ejercicio', 'descripcion', 'tipo']  # Campos que quieres en el formulario
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }


class ComidaForm(forms.ModelForm):
    class Meta:
        model = Nutricion
        fields = ['nombre_comida', 'calorias', 'proteinas', 'grasas', 'carbohidratos']
        labels = {
            'nombre_comida': 'Nombre de Comida',
            'calorias': 'Calorías',
            'proteinas': 'Proteínas (g)',
            'grasas': 'Grasas (g)',
            'carbohidratos': 'Carbohidratos (g)',
        }
        widgets = {
            'nombre_comida': forms.TextInput(attrs={'class': 'form-control'}),
            'calorias': forms.NumberInput(attrs={'class': 'form-control'}),
            'proteinas': forms.NumberInput(attrs={'class': 'form-control'}),
            'grasas': forms.NumberInput(attrs={'class': 'form-control'}),
            'carbohidratos': forms.NumberInput(attrs={'class': 'form-control'}),
        }

