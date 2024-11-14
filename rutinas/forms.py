from django import forms
from rutinas.models import Rutina, EjercicioEnRutina, TipoRutina
from datetime import timedelta

class TipoRutinaModelForm(forms.ModelForm):
    class Meta:
        model = TipoRutina
        fields = ['nombre_tipo', 'descripcion']
        labels = {
            'nombre_tipo': 'Nombre del tipo de rutina',
            'descripcion': 'Descripción'
        }
        widgets = {
            'nombre_tipo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cardio, Fuerza, Flexibilidad...'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe el tipo de rutina...',
                'rows': 4
            })
        }



class RutinaForm(forms.ModelForm):
    duracion_estimada = forms.DurationField(
        help_text="Formato: HH:MM:SS",
        widget=forms.TextInput(attrs={'placeholder': '00:30:00'}),
        initial=timedelta(minutes=30)
    )
    
    # Agregar explícitamente el campo tipo
    tipo = forms.ModelChoiceField(
        queryset=TipoRutina.objects.all().order_by('nombre_tipo'),
        empty_label="Seleccione un tipo de rutina",
        widget=forms.Select(attrs={'class': 'form-control'})
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
        
        # Asegurarse de que el queryset esté actualizado
        self.fields['tipo'].queryset = TipoRutina.objects.all().order_by('nombre_tipo')
        
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
