from django.db import models

class Nutricion(models.Model):
    nombre_comida = models.CharField(max_length=100, null=False, default='')
    calorias = models.IntegerField()
    proteinas = models.DecimalField(max_digits=5, decimal_places=2, null=False, default='')
    grasas = models.DecimalField(max_digits=5, decimal_places=2, null=False, default='')
    carbohidratos = models.DecimalField(max_digits=5, decimal_places=2, null=False, default='' )

    def __str__(self):
        return self.nombre_comida
