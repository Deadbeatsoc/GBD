from django.urls import path
from . import views

app_name = 'rutinas'

urlpatterns = [
    path('rutinas/', views.ver_rutinas, name='index'),  # Ruta para la vista principal de rutina path('agregar/', views.agregar_rutina, name='agregar_rutina'),
    path('agregar_ejercicio/', views.agregar_ejercicio, name='agregar_ejercicio'),
    path('ver_ejercicios/', views.ver_ejercicios, name='ver_ejercicios'),  # Ruta para ver los ejercicioss
]
