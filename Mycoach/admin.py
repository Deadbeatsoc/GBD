from django.contrib import admin
from rutinas.models import (
    Usuario, TipoRutina, Rutina, Ejercicio, RutinaEjercicio,
    Nutricion, ValoracionPersonal, ComentarioEntrenamiento, 
    PlanNutricional, HistorialRutina, ParticipanteRutina, DetalleRutina
)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'rol', 'edad', 'sexo', 'peso_actual', 'altura_actual', 'fecha_nacimiento', 'fecha_registro')
    search_fields = ('nombre', 'email')
    list_filter = ('rol', 'sexo', 'fecha_registro')

@admin.register(TipoRutina)
class TipoRutinaAdmin(admin.ModelAdmin):
    list_display = ('nombre_tipo', 'descripcion')
    search_fields = ('nombre_tipo',)

@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ('nombre_rutina', 'descripcion', 'usuario', 'tipo', 'fecha_inicio')
    search_fields = ('nombre_rutina', 'usuario__nombre')
    list_filter = ('tipo', 'fecha_inicio')

@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('nombre_ejercicio', 'descripcion', 'tipo')
    search_fields = ('nombre_ejercicio',)
    list_filter = ('tipo',)

@admin.register(RutinaEjercicio)
class RutinaEjercicioAdmin(admin.ModelAdmin):
    list_display = ('rutina', 'ejercicio', 'duracion_minutos', 'series', 'repeticiones', 'peso')
    search_fields = ('rutina__nombre_rutina', 'ejercicio__nombre_ejercicio')
    list_filter = ('rutina', 'ejercicio')

@admin.register(Nutricion)
class NutricionAdmin(admin.ModelAdmin):
    list_display = ('nombre_comida', 'calorias', 'proteinas', 'grasas', 'carbohidratos')
    search_fields = ('nombre_comida',)

@admin.register(ValoracionPersonal)
class ValoracionPersonalAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_valoracion', 'masa_corporal', 'grasa_corporal', 'agua_corporal')
    search_fields = ('usuario__nombre',)
    list_filter = ('fecha_valoracion',)

@admin.register(ComentarioEntrenamiento)
class ComentarioEntrenamientoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rutina', 'fecha_comentario', 'comentario')
    search_fields = ('usuario__nombre', 'rutina__nombre_rutina')
    list_filter = ('fecha_comentario',)

@admin.register(PlanNutricional)
class PlanNutricionalAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'comida', 'fecha_plan')
    search_fields = ('usuario__nombre', 'comida__nombre_comida')
    list_filter = ('fecha_plan',)

@admin.register(HistorialRutina)
class HistorialRutinaAdmin(admin.ModelAdmin):
    list_display = ('rutina', 'usuario', 'fecha_realizacion', 'duracion_minutos')
    search_fields = ('usuario__nombre', 'rutina__nombre_rutina')
    list_filter = ('fecha_realizacion',)

@admin.register(ParticipanteRutina)
class ParticipanteRutinaAdmin(admin.ModelAdmin):
    list_display = ('rutina', 'usuario', 'rol')
    search_fields = ('usuario__nombre', 'rutina__nombre_rutina')
    list_filter = ('rol',)

@admin.register(DetalleRutina)
class DetalleRutinaAdmin(admin.ModelAdmin):
    list_display = ('rutina', 'usuario', 'fecha_realizacion', 'progreso', 'observaciones', 'rol')
    search_fields = ('usuario__nombre', 'rutina__nombre_rutina')
    list_filter = ('rol', 'fecha_realizacion')
