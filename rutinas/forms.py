from django import forms
from .models import Rutina

class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['nombre_rutina', 'descripcion', 'fecha_inicio']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        }
