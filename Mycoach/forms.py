from django import forms
from rutinas.models import ValoracionPersonal

class ValoracionPersonalForm(forms.ModelForm):
    class Meta:
        model = ValoracionPersonal
        fields = ['fecha_valoracion', 'masa_corporal', 'grasa_corporal', 'agua_corporal']
        widgets = {
            'fecha_valoracion': forms.DateInput(attrs={'type': 'date'}),
            'masa_corporal': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'grasa_corporal': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'agua_corporal': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }
