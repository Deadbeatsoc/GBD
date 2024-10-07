from django.urls import path
from . import views

app_name = 'rutinas'

urlpatterns = [
    path('rutinas/', views.ver_rutinas, name='index'),  # Ruta para la vista principal de rutinas
]
