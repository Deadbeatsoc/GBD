from django import forms
from .models import Rutina

class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = [
            'nombre',
            'tipo',
            'descripcion',
            'nivel',
            'duracion_estimada',
            'calorias_estimadas',
            'activa'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la rutina'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe la rutina y sus objetivos'
            }),
            'nivel': forms.Select(attrs={
                'class': 'form-control'
            }),
            'duracion_estimada': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'step': '60',  # Para permitir selección por minutos
                'placeholder': 'HH:MM'
            }),
            'calorias_estimadas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Calorías estimadas a quemar'
            }),
            'activa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if usuario:
            self.instance.usuario_creador = usuario

    def clean_duracion_estimada(self):
        duracion = self.cleaned_data.get('duracion_estimada')
        if duracion:
            # Verificar que la duración no sea excesiva (por ejemplo, más de 4 horas)
            from datetime import timedelta
            if duracion > timedelta(hours=4):
                raise forms.ValidationError(
                    "La duración estimada no puede ser mayor a 4 horas"
                )
        return duracion

    def clean_calorias_estimadas(self):
        calorias = self.cleaned_data.get('calorias_estimadas')
        if calorias and calorias > 2000:
            raise forms.ValidationError(
                "Las calorías estimadas parecen muy altas. Por favor verifica."
            )
        return calorias