from django.urls import path
from . import views

app_name = 'controlpesos'

urlpatterns = [
    path('controlpesos/', views.ver_nutriciones, name='index'),
    path('agregar_comida/', views.agregar_comida, name='agregar_comidas'),
    path('ver_nutriciones/', views.ver_nutriciones, name='ver_nutriciones'),
    


]
