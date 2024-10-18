from django import forms
from .models import Rutina

class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['nombre_rutina', 'descripcion', 'fecha_inicio', 'duracion']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'duracion': forms.TimeInput(attrs={'type': 'time'}),
        }
