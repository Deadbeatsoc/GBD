import datetime
from django.db import models

# Modelo de Usuario
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=[('Administrador', 'Administrador'), ('Entrenador', 'Entrenador'), ('Deportista', 'Deportista')])
    edad = models.IntegerField()
    sexo = models.CharField(max_length=20, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')])
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_nacimiento = models.DateField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# Modelo de ComentariosEntrenamientos
class ComentariosEntrenamientos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rutina = models.ForeignKey('Rutina', on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario} sobre la rutina {self.rutina}"

# Modelo de TipoRutina
class TipoRutina(models.Model):
    nombre_tipo = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre_tipo

# Modelo de Rutina
class Rutina(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_rutina = models.ForeignKey(TipoRutina, on_delete=models.CASCADE, null=False, default='' )
    nombre_rutina = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField(default=datetime.date.today)
    duracion = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.nombre_rutina

# Modelo de Ejercicio (general para calentamiento, estiramiento, entrenamiento principal)
class Ejercicio(models.Model):
    nombre_ejercicio = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=100)  # Calentamiento, Estiramiento, Entrenamiento Principal

    def __str__(self):
        return self.nombre_ejercicio

# Modelo de Rutina_Calentamiento
class RutinaCalentamiento(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    duracion_minutos = models.IntegerField()
    repeticiones = models.IntegerField()

    def __str__(self):
        return f"Calentamiento de {self.rutina}"

# Modelo de Rutina_Estiramiento
class RutinaEstiramiento(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    duracion_minutos = models.IntegerField()
    repeticiones = models.IntegerField()

    def __str__(self):
        return f"Estiramiento de {self.rutina}"

# Modelo de Rutina_EntrenamientoPrincipal
class RutinaEntrenamientoPrincipal(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    series = models.IntegerField()
    repeticiones = models.IntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Entrenamiento principal de {self.rutina}"

# Modelo de Nutrición
class Nutricion(models.Model):
    nombre_comida = models.CharField(max_length=100)
    calorias = models.IntegerField()
    proteinas = models.DecimalField(max_digits=5, decimal_places=2)
    grasas = models.DecimalField(max_digits=5, decimal_places=2)
    carbohidratos = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nombre_comida

# Modelo de ValoracionesPersonales
class ValoracionesPersonales(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_valoracion = models.DateField()
    grasa_corporal = models.DecimalField(max_digits=5, decimal_places=2)
    agua_corporal = models.DecimalField(max_digits=5, decimal_places=2)
    comentarios = models.TextField()

    def __str__(self):
        return f"Valoración de {self.usuario}"

# Modelo de MasaSegmental
class MasaSegmental(models.Model):
    valoracion = models.ForeignKey(ValoracionesPersonales, on_delete=models.CASCADE)
    musculo = models.CharField(max_length=100, choices=[('Brazo Derecho', 'Brazo Derecho'), ('Brazo Izquierdo', 'Brazo Izquierdo'), ('Pierna Derecha', 'Pierna Derecha'), ('Pierna Izquierda', 'Pierna Izquierda'), ('Tronco', 'Tronco')])
    masa = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Masa segmental de {self.musculo} - Valoración {self.valoracion}"
