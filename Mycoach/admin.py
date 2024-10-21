from django.contrib import admin
from rutinas.models import Usuario, ComentariosEntrenamientos, TipoRutina, Rutina, Ejercicio, RutinaCalentamiento, RutinaEstiramiento, RutinaEntrenamientoPrincipal, Nutricion, ValoracionesPersonales, MasaSegmental, Coach, Deportista

# Personalización del administrador del modelo Usuario
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'rol', 'edad', 'sexo', 'peso', 'altura', 'fecha_nacimiento', 'fecha_registro')
    search_fields = ('nombre', 'email')
    list_filter = ('rol', 'sexo')

# Personalización del administrador del modelo ComentariosEntrenamientos
@admin.register(ComentariosEntrenamientos)
class ComentariosEntrenamientosAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rutina', 'comentario', 'fecha_comentario')
    search_fields = ('usuario__nombre', 'rutina__nombre_rutina')

# Personalización del administrador del modelo TipoRutina
@admin.register(TipoRutina)
class TipoRutinaAdmin(admin.ModelAdmin):
    list_display = ('nombre_tipo', 'descripcion')
    search_fields = ('nombre_tipo',)

# Personalización del administrador del modelo Rutina
@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ('nombre_rutina', 'usuario', 'tipo_rutina', 'fecha_inicio', 'duracion')
    search_fields = ('nombre_rutina', 'usuario__nombre')
    list_filter = ('tipo_rutina',)

# Personalización del administrador del modelo Ejercicio
@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('nombre_ejercicio', 'tipo')
    search_fields = ('nombre_ejercicio', 'tipo')
    list_filter = ('tipo',)

# Personalización del administrador del modelo RutinaCalentamiento
@admin.register(RutinaCalentamiento)
class RutinaCalentamientoAdmin(admin.ModelAdmin):
    list_display = ('rutina', 'ejercicio', 'duracion_minutos', 'repeticiones')
    search_fields = ('rutina__nombre_rutina', 'ejercicio__nombre_ejercicio')

# Personalización del administrador del modelo RutinaEstiramiento
@admin.register(RutinaEstiramiento)
class RutinaEstiramientoAdmin(admin.ModelAdmin):
    list_display = ('rutina', 'ejercicio', 'duracion_minutos', 'repeticiones')
    search_fields = ('rutina__nombre_rutina', 'ejercicio__nombre_ejercicio')

# Personalización del administrador del modelo RutinaEntrenamientoPrincipal
@admin.register(RutinaEntrenamientoPrincipal)
class RutinaEntrenamientoPrincipalAdmin(admin.ModelAdmin):
    list_display = ('rutina', 'ejercicio', 'series', 'repeticiones', 'peso')
    search_fields = ('rutina__nombre_rutina', 'ejercicio__nombre_ejercicio')

# Personalización del administrador del modelo Nutricion
@admin.register(Nutricion)
class NutricionAdmin(admin.ModelAdmin):
    list_display = ('nombre_comida', 'calorias', 'proteinas', 'grasas', 'carbohidratos')
    search_fields = ('nombre_comida',)

# Personalización del administrador del modelo ValoracionesPersonales
@admin.register(ValoracionesPersonales)
class ValoracionesPersonalesAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_valoracion', 'grasa_corporal', 'agua_corporal')
    search_fields = ('usuario__nombre',)

# Personalización del administrador del modelo MasaSegmental
@admin.register(MasaSegmental)
class MasaSegmentalAdmin(admin.ModelAdmin):
    list_display = ('valoracion', 'musculo', 'masa')
    search_fields = ('valoracion__usuario__nombre', 'musculo')

# Personalización del administrador del modelo Coach
@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especialidad')
    search_fields = ('nombre', 'especialidad')

# Personalización del administrador del modelo Deportista
@admin.register(Deportista)
class DeportistaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'edad', 'deporte', 'coach')
    search_fields = ('nombre', 'deporte', 'coach__nombre')
    list_filter = ('deporte',)

