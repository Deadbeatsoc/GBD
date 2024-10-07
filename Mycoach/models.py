from django.db import models

# Create your models here.
from django.db import models

class Usuario(models.Model):
    ROLES = [
        ('Entrenador', 'Entrenador'),
        ('Deportista', 'Deportista'),
    ]
    SEXO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Otro', 'Otro'),
    ]
    
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=ROLES)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=4, decimal_places=2)
    fecha_nacimiento = models.DateField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.nombre




class ValoracionPersonal(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_valoracion = models.DateField()
    masa_segmental = models.DecimalField(max_digits=5, decimal_places=2)
    grasa_corporal = models.DecimalField(max_digits=5, decimal_places=2)

    def _str_(self):
        return f'Valoración {self.fecha_valoracion} - Usuario: {self.usuario.nombre}'

