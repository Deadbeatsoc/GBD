from django.urls import path

from Mysite.views import logout_view
from . import views

app_name = 'mycoach'

urlpatterns = [
    path('mycoach/', views.ver_usuarios, name='index'),
    path('registrar_usuario/', views.registrar_usuario, name='crear_usuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
