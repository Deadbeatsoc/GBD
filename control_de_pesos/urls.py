from django.urls import path
from . import views

app_name = 'controlpesos'

urlpatterns = [
    path('controlpesos/', views.ver_nutricion, name='index'),
]
