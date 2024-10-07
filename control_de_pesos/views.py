from django.shortcuts import render

# Create your views here.
from .models import Nutricion

def ver_nutricion(request):
    nutricion = Nutricion.objects.all()  # Obtén todos los datos de nutrición
    return render(request, 'nutricion.html', {'nutricion': nutricion})



def index(request):
    return render(request, 'nutricion.html')  # Ruta específica a la plantilla

