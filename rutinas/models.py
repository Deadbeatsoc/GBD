from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, contrasena=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un email')
        email = self.normalize_email(email)
        usuario = self.model(email=email, nombre=nombre, **extra_fields)
        usuario.set_password(contrasena)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, nombre, contrasena=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, nombre, contrasena, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    ROL_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Entrenador', 'Entrenador'),
        ('Deportista', 'Deportista')
    ]
    SEXO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Otro', 'Otro')
    ]

    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=15, choices=ROL_CHOICES)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    peso_actual = models.DecimalField(max_digits=5, decimal_places=2)
    altura_actual = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    fecha_nacimiento = models.DateField()
    fecha_registro = models.DateTimeField(default=timezone.now)
    password = models.CharField(max_length=128, default='defaultpassword')

    
    # Campos requeridos para el modelo de usuario en Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Configuración de USERNAME_FIELD y REQUIRED_FIELDS
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'rol', 'edad', 'sexo']

    objects = UsuarioManager()

    def __str__(self):
        return self.nombre

class TipoRutina(models.Model):
    nombre_tipo = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre_tipo


class Rutina(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoRutina, on_delete=models.CASCADE, null=True, blank=True)
    nombre_rutina = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()

    def __str__(self):
        return self.nombre_rutina


class Ejercicio(models.Model):
    TIPO_CHOICES = [
        ('Calentamiento', 'Calentamiento'),
        ('Estiramiento', 'Estiramiento'),
        ('EntrenamientoPrincipal', 'Entrenamiento Principal')
    ]

    nombre_ejercicio = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)

    def __str__(self):
        return self.nombre_ejercicio


class RutinaEjercicio(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    duracion_minutos = models.IntegerField()
    series = models.IntegerField()
    repeticiones = models.IntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)


class Nutricion(models.Model):
    nombre_comida = models.CharField(max_length=100)
    calorias = models.IntegerField()
    proteinas = models.DecimalField(max_digits=5, decimal_places=2)
    grasas = models.DecimalField(max_digits=5, decimal_places=2)
    carbohidratos = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nombre_comida


class ValoracionPersonal(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_valoracion = models.DateField()
    masa_corporal = models.DecimalField(max_digits=5, decimal_places=2)
    grasa_corporal = models.DecimalField(max_digits=5, decimal_places=2)
    agua_corporal = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Valoración de {self.usuario} en {self.fecha_valoracion}"

class ComentarioEntrenamiento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)


class PlanNutricional(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comida = models.ForeignKey(Nutricion, on_delete=models.CASCADE)
    fecha_plan = models.DateField()


class HistorialRutina(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_realizacion = models.DateField()
    duracion_minutos = models.IntegerField()


class ParticipanteRutina(models.Model):
    ROL_CHOICES = [
        ('Entrenador', 'Entrenador'),
        ('Deportista', 'Deportista')
    ]

    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)


class DetalleRutina(models.Model):
    ROL_CHOICES = [
        ('Participante', 'Participante'),
        ('Observador', 'Observador'),
        ('Coach', 'Coach')
    ]

    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_realizacion = models.DateField()
    progreso = models.CharField(max_length=100)
    observaciones = models.TextField()
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
