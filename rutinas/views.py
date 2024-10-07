from django.shortcuts import render
from .models import Rutina

def ver_rutinas(request):
    rutinas = Rutina.objects.all()  # Obtén todas las rutinas de la base de datos
    return render(request, 'rutinas.html', {'rutinas': rutinas})



def index(request):
    return render(request, 'rutinas/rutinas.html')  # Ruta específica a la plantilla de rutinas

