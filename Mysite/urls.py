"""
URL configuration for Mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from .views import logout_view 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Página principal
    path('rutinas/', include('rutinas.urls')),  # Ruta para la app de Rutinas
    path('mycoach/', include('Mycoach.urls')),  # Ruta para la app de MyCoach
    path('controlpesos/', include('control_de_pesos.urls')),  # Ruta para la app de Control de Pesospath('', include('rutinas.urls')),
    path('crear_usuario/', views.registrar_usuario, name='crear_usuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('agregar/', views.agregar_rutina, name='agregar_rutina'),
    path('agregar_ejercicio/', views.agregar_ejercicio, name='agregar_ejercicio'),
    path('ver_ejercicios/', views.ver_ejercicios, name='ver_ejercicios'),  # Ruta para ver los ejercicios
    path('agregar_comida/', views.agregar_comida, name='agregar_comida'),
    path('ver_nutriciones/', views.ver_nutriciones, name='ver_nutriciones'),  # Ruta para ver la lista de nutriciones


]


