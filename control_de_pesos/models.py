from django.db import models

# Create your models here.



class Nutricion(models.Model):
    nombre_comida = models.CharField(max_length=100)
    calorias = models.IntegerField()
    proteinas = models.DecimalField(max_digits=5, decimal_places=2)
    grasas = models.DecimalField(max_digits=5, decimal_places=2)
    carbohidratos = models.DecimalField(max_digits=5, decimal_places=2)

    def _str_(self):
        return self.nombre_comida

