from django.urls import path
from .views import cerrar_sesion
from . import views

app_name = 'mycoach'

urlpatterns = [
    path('mycoach/', views.ver_usuarios, name='index'),
    path('registrar_usuario/', views.registrar_usuario, name='crear_usuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', cerrar_sesion, name='logout'),
]
