from django import forms
from rutinas.models import Rutina, EjercicioEnRutina, TipoRutina
from datetime import timedelta

class RutinaForm(forms.ModelForm):
    duracion_estimada = forms.DurationField(
        help_text="Formato: HH:MM:SS",
        widget=forms.TextInput(attrs={'placeholder': '00:30:00'}),
        initial=timedelta(minutes=30)
    )
    
    class Meta:
        model = Rutina
        fields = ['nombre', 'tipo', 'descripcion', 'nivel', 'duracion_estimada', 'calorias_estimadas']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'calorias_estimadas': forms.NumberInput(attrs={'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RutinaForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.usuario_creador = user

class EjercicioEnRutinaForm(forms.ModelForm):
    descanso = forms.DurationField(
        help_text="Formato: MM:SS",
        widget=forms.TextInput(attrs={'placeholder': '01:30'}),
        initial=timedelta(seconds=90)
    )
    
    class Meta:
        model = EjercicioEnRutina
        fields = ['nombre_ejercicio', 'descripcion', 'series', 'repeticiones', 'descanso', 'notas']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'notas': forms.Textarea(attrs={'rows': 2}),
            'series': forms.NumberInput(attrs={'min': 1}),
            'repeticiones': forms.NumberInput(attrs={'min': 1}),
        }

class RutinaExistenteForm(forms.Form):
    rutina = forms.ModelChoiceField(
        queryset=Rutina.objects.filter(activa=True),
        empty_label="Seleccione una rutina",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
