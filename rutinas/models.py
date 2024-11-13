from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.contrib.auth.models import AbstractUser



class Usuario(models.Model):
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
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    rol = models.CharField(max_length=15, choices=ROL_CHOICES)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    peso_actual = models.DecimalField(max_digits=5, decimal_places=2)
    altura_actual = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    fecha_nacimiento = models.DateField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username






class TipoRutina(models.Model):
    nombre_tipo = models.CharField(max_length=100)
    descripcion = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tipo de Rutina"
        verbose_name_plural = "Tipos de Rutinas"
        ordering = ['nombre_tipo']

    def __str__(self):
        return self.nombre_tipo

class Rutina(models.Model):
    NIVEL_CHOICES = [
        ('Principiante', 'Principiante'),
        ('Intermedio', 'Intermedio'),
        ('Avanzado', 'Avanzado')
    ]

    nombre = models.CharField(max_length=200, default="sin nombre")
    tipo = models.ForeignKey(TipoRutina, on_delete=models.CASCADE, 
                           related_name='rutinas',
                           verbose_name="Tipo de Rutina",
                           default=1)
    descripcion = models.TextField()
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='Principiante')
    duracion_estimada = models.DurationField(help_text="Duración estimada de la rutina", default=0)
    calorias_estimadas = models.PositiveIntegerField(
        help_text="Calorías estimadas a quemar",
        null=True,
        blank=True
    )
    usuario_creador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rutinas_creadas',
        default="no se conoce"
    )
    fecha_creacion = models.DateTimeField(default=timezone.now)
    ultima_modificacion = models.DateTimeField(auto_now=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Rutina"
        verbose_name_plural = "Rutinas"
        ordering = ['-fecha_creacion']
        
    def __str__(self):
        return f"{self.nombre} - {self.tipo}"

    def get_duracion_en_minutos(self):
        return self.duracion_estimada.total_seconds() / 60

    def esta_vigente(self):
        """Verifica si la rutina está activa y no es muy antigua"""
        tiempo_limite = timezone.now() - timezone.timedelta(days=365)
        return self.activa and self.fecha_creacion > tiempo_limite

class EjercicioEnRutina(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name='ejercicios')
    nombre_ejercicio = models.CharField(max_length=200)
    descripcion = models.TextField()
    series = models.PositiveIntegerField()
    repeticiones = models.PositiveIntegerField()
    descanso = models.DurationField(help_text="Tiempo de descanso entre series")
    orden = models.PositiveIntegerField(help_text="Orden del ejercicio en la rutina")
    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = "Ejercicio en Rutina"
        verbose_name_plural = "Ejercicios en Rutina"
        ordering = ['orden']
        unique_together = ['rutina', 'orden']  # Evita duplicados en el orden

    def __str__(self):
        return f"{self.nombre_ejercicio} - {self.series}x{self.repeticiones}"

class Nutricion(models.Model):
    nombre_comida = models.CharField(max_length=100)
    calorias = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Cantidad de calorías por 100g"
    )
    proteinas = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Gramos de proteína por 100g"
    )
    grasas = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Gramos de grasas por 100g"
    )
    carbohidratos = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Gramos de carbohidratos por 100g"
    )
    porcion_recomendada = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Porción recomendada en gramos",
        default=100.00
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Alimento"
        verbose_name_plural = "Alimentos"
        ordering = ['nombre_comida']

    def __str__(self):
        return f"{self.nombre_comida} ({self.calorias} kcal/100g)"

    def get_macros_por_porcion(self):
        factor = self.porcion_recomendada / 100
        return {
            'calorias': self.calorias * factor,
            'proteinas': self.proteinas * factor,
            'grasas': self.grasas * factor,
            'carbohidratos': self.carbohidratos * factor
        }

class ValoracionPersonal(models.Model):
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='valoraciones'
    )
    fecha_valoracion = models.DateField()
    masa_corporal = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('30.00')),
            MaxValueValidator(Decimal('300.00'))
        ],
        help_text="Peso en kilogramos",
        default=0
    )
    grasa_corporal = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('3.00')),
            MaxValueValidator(Decimal('60.00'))
        ],
        help_text="Porcentaje de grasa corporal"
    )
    agua_corporal = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('20.00')),
            MaxValueValidator(Decimal('80.00'))
        ],
        help_text="Porcentaje de agua corporal"
    )
    notas = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Valoración Personal"
        verbose_name_plural = "Valoraciones Personales"
        ordering = ['-fecha_valoracion']
        unique_together = ['usuario', 'fecha_valoracion']  # Evita duplicados en la misma fecha

    def __str__(self):
        return f"Valoración de {self.usuario} - {self.fecha_valoracion}"

    def calcular_imc(self):
        """Calcula el Índice de Masa Corporal"""
        altura = self.usuario.altura_actual
        if not altura:
            return None
        return self.masa_corporal / (altura * altura)

    def get_estado_imc(self):
        """Retorna la clasificación del IMC"""
        imc = self.calcular_imc()
        if not imc:
            return "No disponible"
        if imc < 18.5:
            return "Bajo peso"
        elif imc < 25:
            return "Peso normal"
        elif imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidad"
        


class ComentarioEntrenamiento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)


class PlanNutricional(models.Model):
    COMIDA_CHOICES = [
        ('Desayuno', 'Desayuno'),
        ('Almuerzo', 'Almuerzo'),
        ('Cena', 'Cena'),
        ('Snack', 'Snack')
    ]

    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='planes_nutricionales'
    )
    fecha_plan = models.DateField()
    alimentos = models.ManyToManyField(
        Nutricion,
        through='DetallePlanNutricional'
    )
    notas = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
   
    
    class Meta:
        verbose_name = "Plan Nutricional"
        verbose_name_plural = "Planes Nutricionales"
        ordering = ['-fecha_plan']
        unique_together = ['usuario', 'fecha_plan']

    def __str__(self):
        return f"Plan de {self.usuario} - {self.fecha_plan} "

    def get_total_calorias(self):
        return sum(detalle.get_calorias() 
                  for detalle in self.detalles.all())
    




class DetallePlanNutricional(models.Model):
    plan = models.ForeignKey(
        PlanNutricional,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    alimento = models.ForeignKey(
        Nutricion,
        on_delete=models.CASCADE,
        related_name='+'
    )
    cantidad = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Cantidad en gramos"
    )
    orden = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['orden']
        unique_together = ['plan', 'alimento']

    def get_calorias(self):
        return (self.alimento.calorias * self.cantidad) / 100


class HistorialRutina(models.Model):
    rutina = models.ForeignKey(
        Rutina, 
        on_delete=models.CASCADE,
        related_name='historiales'
    )
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='historiales_rutina'
    )
    fecha_realizacion = models.DateField()
    duracion_minutos = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(480)  # 8 horas máximo
        ]
    )
    calorias_quemadas = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Calorías estimadas quemadas durante la rutina"
    )
    nivel_esfuerzo = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        help_text="Nivel de esfuerzo percibido (1-10)",
        default=1
    )
    completada = models.BooleanField(default=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha_realizacion']
        verbose_name = "Historial de Rutina"
        verbose_name_plural = "Historiales de Rutina"

    def __str__(self):
        return f"{self.usuario} - {self.rutina.nombre} ({self.fecha_realizacion})"

    def get_eficiencia(self):
        """Calcula la eficiencia basada en la duración estimada vs real"""
        if not self.rutina.duracion_estimada:
            return None
        duracion_estimada = self.rutina.get_duracion_en_minutos()
        return (duracion_estimada / self.duracion_minutos) * 100


class ParticipanteRutina(models.Model):
    ROL_CHOICES = [
        ('Entrenador', 'Entrenador'),
        ('Deportista', 'Deportista')
    ]

    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)


class DetalleRutina(models.Model):
    ROL_CHOICES = [
        ('Participante', 'Participante'),
        ('Observador', 'Observador'),
        ('Coach', 'Coach')
    ]

    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_realizacion = models.DateField()
    progreso = models.CharField(max_length=100)
    observaciones = models.TextField()
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)