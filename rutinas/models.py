from django.db import models

# Create your models here.
from django.db import models

from Mycoach.models import Usuario


class Rutina(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre_rutina = models.CharField(max_length=100)
    descripcion = models.TextField()

    def _str_(self):
        return self.nombre_rutina


class Calentamiento(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    ejercicio = models.CharField(max_length=100)
    duracion_minutos = models.IntegerField()
    repeticiones = models.IntegerField()

    def _str_(self):
        return self.ejercicio


class Estiramiento(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    ejercicio = models.CharField(max_length=100)
    duracion_minutos = models.IntegerField()
    repeticiones = models.IntegerField()

    def _str_(self):
        return self.ejercicio


class EntrenamientoPrincipal(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    ejercicio = models.CharField(max_length=100)
    series = models.IntegerField()
    repeticiones = models.IntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    intensidad = models.IntegerField()

    def _str_(self):
        return self.ejercicio




class ComentarioEntrenamiento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f'Comentario de {self.usuario.nombre} en {self.rutina.nombre_rutina}'