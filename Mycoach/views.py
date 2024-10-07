from django.shortcuts import render
from .models import Usuario

def ver_usuarios(request):
    usuarios = Usuario.objects.all()  # Obtén todos los usuarios de la base de datos
    return render(request, 'usuarios.html', {'usuarios': usuarios})



def index(request):
    return render(request, 'usuarios.html')
