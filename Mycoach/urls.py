from django.urls import path
from . import views

app_name = 'mycoach'

urlpatterns = [
    path('mycoach/', views.ver_usuarios, name='index'),
]
