from django import forms
from rutinas.models import EjercicioEnRutina, Nutricion,ValoracionPersonal  # Para encriptar la contraseña
from rutinas.models import User,Usuario



from django.contrib.auth.forms import UserCreationForm
from rutinas.models import Usuario

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        usuario = Usuario(
            user=user,
            rol=self.cleaned_data['rol'],
            edad=self.cleaned_data['edad'],
            sexo=self.cleaned_data['sexo'],
            peso_actual=self.cleaned_data['peso_actual'],
            altura_actual=self.cleaned_data['altura_actual'],
            fecha_nacimiento=self.cleaned_data['fecha_nacimiento']
        )
        if commit:
            user.save()
            usuario.save()
        return user
    

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ComidaForm(forms.ModelForm):
    class Meta:
        model = Nutricion
        fields = [
            'nombre_comida',
            'calorias',
            'proteinas',
            'grasas',
            'carbohidratos',
            'porcion_recomendada'
        ]
        widgets = {
            'nombre_comida': forms.TextInput(attrs={'class': 'form-control'}),
            'calorias': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'proteinas': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'grasas': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'carbohidratos': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'porcion_recomendada': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'})
        }
        
    def clean(self):
        cleaned_data = super().clean()
        # Validar que la suma de macronutrientes no exceda 100g por cada 100g de alimento
        proteinas = cleaned_data.get('proteinas', 0)
        grasas = cleaned_data.get('grasas', 0)
        carbohidratos = cleaned_data.get('carbohidratos', 0)
        
        if proteinas and grasas and carbohidratos:
            total = proteinas + grasas + carbohidratos
            if total > 100:
                raise forms.ValidationError(
                    "La suma de proteínas, grasas y carbohidratos no puede exceder 100g por cada 100g de alimento"
                )
        return cleaned_data

class EjercicioForm(forms.ModelForm):
    class Meta:
        model = EjercicioEnRutina
        fields = [
            'nombre_ejercicio',
            'descripcion',
            'series',
            'repeticiones',
            'descanso',
            'orden',
            'notas'
        ]
        widgets = {
            'nombre_ejercicio': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'series': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'repeticiones': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'descanso': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'step': '1'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }

    def __init__(self, *args, **kwargs):
        rutina = kwargs.pop('rutina', None)
        super().__init__(*args, **kwargs)
        if rutina:
            self.instance.rutina = rutina
            # Obtener el último orden y sumar 1 para el valor por defecto
            ultimo_orden = EjercicioEnRutina.objects.filter(rutina=rutina).count()
            self.fields['orden'].initial = ultimo_orden + 1

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
            'fecha_valoracion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'masa_corporal': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '30',
                'max': '300',
                'step': '0.01'
            }),
            'grasa_corporal': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '3',
                'max': '60',
                'step': '0.01'
            }),
            'agua_corporal': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '20',
                'max': '80',
                'step': '0.01'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            })
        }

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if usuario:
            self.instance.usuario = usuario