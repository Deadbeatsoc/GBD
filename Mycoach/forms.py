from django import forms
from rutinas.models import ValoracionPersonal
from django.utils import timezone



class ValoracionPersonalForm(forms.ModelForm):
    class Meta:
        model = ValoracionPersonal
        fields = [
            'fecha_valoracion',
            'masa_corporal',
            'grasa_corporal',
            'agua_corporal',
            'notas'
        ]
        widgets = {
            'fecha_valoracion': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'masa_corporal': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.1',
                    'min': '30',
                    'max': '300'
                }
            ),
            'grasa_corporal': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.1',
                    'min': '3',
                    'max': '60'
                }
            ),
            'agua_corporal': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.1',
                    'min': '20',
                    'max': '80'
                }
            ),
            'notas': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Añade notas adicionales sobre tu valoración...'
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_valoracion = cleaned_data.get('fecha_valoracion')
        
        if fecha_valoracion and fecha_valoracion > timezone.now().date():
            raise forms.ValidationError(
                "La fecha de valoración no puede ser futura."
            )
        
        return cleaned_data