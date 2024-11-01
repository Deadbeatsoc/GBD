# forms.py

from django import forms
from rutinas import models
from rutinas.models import ValoracionPersonal

class ValoracionForm(forms.ModelForm):
    class Meta:
        model = ValoracionPersonal
        fields = ['masa_segmental', 'grasa_corporal', 'agua_corporal', 'fecha_valoracion']
        widgets = {
            'fecha_valoracion': forms.DateInput(attrs={'type': 'date'}),
        }




