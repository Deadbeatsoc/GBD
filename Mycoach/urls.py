from django.urls import path
from .views import cerrar_sesion
from . import views


app_name = 'mycoach'

urlpatterns = [
    path('mycoach/', views.mi_informacion, name='index'),
    path('registrar_usuario/', views.registrar_usuario, name='crear_usuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('agregar_valoracion/', views.agregar_valoracion, name='agregar_valoraciones'),
    path('rutinas/', views.lista_rutinas, name='lista_rutinas'),
    path('rutinas/asignar/', views.asignar_rutina, name='asignar_rutina'),
    path('rutinas/editar/<int:pk>/', views.editar_rutina, name='editar_rutina'),
    path('rutinas/eliminar/<int:pk>/', views.eliminar_rutina, name='eliminar_rutina'),
    path('planes-nutricionales/', views.lista_planes_nutricionales, name='lista_planes_nutricionales'),
    path('planes-nutricionales/asignar/', views.asignar_plan_nutricional, name='asignar_plan_nutricional'),
    path('planes-nutricionales/editar/<int:pk>/', views.editar_nutricion, name='editar_plan_nutricional'),
    path('planes-nutricionales/eliminar/<int:pk>/', views.eliminar_nutricion, name='eliminar_plan_nutricional'),
    path('valoraciones/<int:pk>/', views.ver_valoracion, name='ver_valoraciones'),   
    path('valoraciones/agregar/', views.agregar_valoracion, name='agregar_valoracion'),
    path('valoraciones/editar/<int:pk>/', views.editar_valoracion, name='editar_valoracion'),

]
