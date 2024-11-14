from django.urls import path
from . import views

app_name = 'rutinas'

urlpatterns = [
    path('rutinas/', views.ver_rutinas, name='index'),  # Ruta para la vista principal de rutina path('agregar/', views.agregar_rutina, name='agregar_rutina'),
    path('agregar-existente/', views.agregar_rutina_existente, name='agregar_rutina_existente'),
    path('crear/', views.crear_rutina, name='crear_rutina'),
    path('crear-ejercicio/', views.crear_ejercicio, name='crear_ejercicio'),
    path('ejercicio/<int:ejercicio_id>/eliminar/', views.eliminar_ejercicio, name='eliminar_ejercicio'),
    path('rutina/<int:rutina_id>/ejercicios/', views.ver_ejercicios_rutina, name='ver_ejercicios_rutina'),
    path('agregar-ejercicio-rutina/', views.agregar_ejercicio_rutina, name='agregar_ejercicio_rutina'),
    path('actualizar-orden-ejercicios/', views.actualizar_orden_ejercicios, name='actualizar_orden_ejercicios'),
    path('crear-tipo-rutina/', views.crear_tipo_rutina, name='crear_tipo_rutina'),

]
