from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.contrib.auth.models import User
from rutinas.models import (
    TipoRutina, Rutina, EjercicioEnRutina, 
    Nutricion, ValoracionPersonal, PlanNutricional,
    DetallePlanNutricional, HistorialRutina, ComentarioEntrenamiento,
    ParticipanteRutina, DetalleRutina,Usuario
)

@admin.register(Usuario)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_role', 'edad', 'fecha_registro', 'user__is_active', 'user__is_staff')
    list_filter = ('rol', 'user__is_active', 'user__is_staff', 'fecha_registro')
    search_fields = ('user__username', 'user__email')
    ordering = ('-fecha_registro',)
    readonly_fields = ('fecha_registro',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('user__username', 'user__email', 'fecha_nacimiento', 'edad', 'sexo')
        }),
        ('Measurements', {
            'fields': ('peso_actual', 'altura_actual')
        }),
        ('Role and Permissions', {
            'fields': ('rol', 'user__is_active', 'user__is_staff', 'user__is_superuser')
        }),
    )

    def get_role(self, obj):
        return obj.rol
    get_role.short_description = 'Role'

    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'

    def save_model(self, request, obj, form, change):
        if change:
            # Update the related User object
            obj.user.username = obj.user.username
            obj.user.email = obj.user.email
            obj.user.is_active = obj.user.is_active
            obj.user.is_staff = obj.user.is_staff
            obj.user.save()
        super().save_model(request, obj, form, change)

# Customize admin site
admin.site.site_header = "Training Management System"
admin.site.site_title = "Administration Panel"
admin.site.index_title = "Welcome to the Management System"

# Custom admin dashboard
class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # Here you can customize the order and presentation of the apps
        return app_list

    def index(self, request, extra_context=None):
        # Dashboard statistics
        extra_context = extra_context or {}
        extra_context['total_users'] = Usuario.objects.count()
        extra_context['total_athletes'] = Usuario.objects.filter(rol='Deportista').count()
        extra_context['total_coaches'] = Usuario.objects.filter(rol='Entrenador').count()
        extra_context['total_admins'] = Usuario.objects.filter(rol='Administrador').count()
        extra_context['new_users'] = Usuario.objects.filter(
            fecha_registro__gte=timezone.now() - timezone.timedelta(days=30)
        ).count()
        
        return super().index(request, extra_context)



@admin.register(TipoRutina)
class TipoRutinaAdmin(admin.ModelAdmin):
    list_display = ('nombre_tipo', 'get_routines_count', 'created_at')
    search_fields = ('nombre_tipo',)
    ordering = ('nombre_tipo',)

    def get_routines_count(self, obj):
        return obj.rutinas.count()
    get_routines_count.short_description = 'Routines Count'

class EjercicioEnRutinaInline(admin.TabularInline):
    model = EjercicioEnRutina
    extra = 1
    ordering = ('orden',)

@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'nivel', 'usuario_creador', 
                   'get_exercises_count', 'fecha_creacion', 'activa')
    list_filter = ('nivel', 'tipo', 'activa', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion', 'usuario_creador__username')
    inlines = [EjercicioEnRutinaInline]
    readonly_fields = ('fecha_creacion', 'ultima_modificacion')
    
    def get_exercises_count(self, obj):
        return obj.ejercicios.count()
    get_exercises_count.short_description = 'Exercises'

@admin.register(Nutricion)
class NutricionAdmin(admin.ModelAdmin):
    list_display = ('nombre_comida', 'calorias', 'proteinas', 
                   'grasas', 'carbohidratos')
    search_fields = ('nombre_comida',)
    ordering = ('nombre_comida',)
    list_filter = ('created_at',)

class DetallePlanNutricionalInline(admin.TabularInline):
    model = DetallePlanNutricional
    extra = 1

@admin.register(PlanNutricional)
class PlanNutricionalAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_plan', 'get_total_calories')
    list_filter = ('fecha_plan',)
    search_fields = ('usuario__username', 'notas')
    inlines = [DetallePlanNutricionalInline]

    def get_total_calories(self, obj):
        return f"{obj.get_total_calorias():.0f} kcal"
    get_total_calories.short_description = 'Total Calories'


@admin.register(ValoracionPersonal)
class ValoracionPersonalAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_valoracion', 'masa_corporal', 
                   'grasa_corporal', 'get_bmi')
    list_filter = ('fecha_valoracion',)
    search_fields = ('usuario__username',)
    readonly_fields = ('created_at',)

    def get_bmi(self, obj):
        bmi = obj.calcular_imc()
        if bmi:
            estado = obj.get_estado_imc()
            color = {
                'Bajo peso': 'orange',
                'Peso normal': 'green',
                'Sobrepeso': 'orange',
                'Obesidad': 'red'
            }.get(estado, 'black')
            return format_html('<span style="color: {};">{:.1f} ({})</span>', 
                             color, bmi, estado)
        return "N/A"
    get_bmi.short_description = 'BMI'

@admin.register(HistorialRutina)
class HistorialRutinaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rutina', 'fecha_realizacion', 
                   'duracion_minutos', 'completada')
    list_filter = ('completada', 'fecha_realizacion')
    search_fields = ('usuario__username', 'rutina__nombre')
    readonly_fields = ('get_efficiency',)

    def get_efficiency(self, obj):
        efficiency = obj.get_eficiencia()
        if efficiency is not None:
            return f"{efficiency:.1f}%"
        return "N/A"
    get_efficiency.short_description = 'Efficiency'

@admin.register(ComentarioEntrenamiento)
class ComentarioEntrenamientoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rutina', 'fecha_comentario')
    list_filter = ('fecha_comentario',)
    search_fields = ('usuario__username', 'comentario')
    readonly_fields = ('fecha_comentario',)

@admin.register(ParticipanteRutina)
class ParticipanteRutinaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rutina', 'rol')
    list_filter = ('rol',)
    search_fields = ('usuario__username', 'rutina__nombre')

@admin.register(DetalleRutina)
class DetalleRutinaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rutina', 'fecha_realizacion', 'rol', 'progreso')
    list_filter = ('rol', 'fecha_realizacion')
    search_fields = ('usuario__username', 'rutina__nombre', 'observaciones')

# Customize admin site
admin.site.site_header = "Training Management System"
admin.site.site_title = "Administration Panel"
admin.site.index_title = "Welcome to the Management System"

# Custom admin dashboard
class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # Here you can customize the order and presentation of the apps
        return app_list

    def index(self, request, extra_context=None):
        # Dashboard statistics
        extra_context = extra_context or {}
        extra_context['total_users'] = User.objects.count()
        extra_context['total_routines'] = Rutina.objects.count()
        extra_context['active_routines'] = Rutina.objects.filter(activa=True).count()
        extra_context['new_users'] = User.objects.filter(
            date_joined__gte=timezone.now() - timezone.timedelta(days=30)
        ).count()
        
        return super().index(request, extra_context)