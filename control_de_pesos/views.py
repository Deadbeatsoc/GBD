from django.shortcuts import  redirect, render

from Mysite.forms import ComidaForm


# Create your views here.
from .models import Nutricion







def index(request):
    return render(request, 'ver_nutriciones.html')  # Ruta específica a la plantilla





def ver_nutriciones(request):
    nutriciones = Nutricion.objects.all()
    return render(request, 'ver_nutriciones.html', {'nutriciones': nutriciones})

def ver_nutricion(request):
    nutriciones = Nutricion.objects.all()
    return render(request, 'ver_nutriciones.html', {'nutriciones': nutriciones})



def agregar_comida(request):
    if request.method == 'POST':
        form = ComidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_nutriciones')  # Redirigir a la lista de nutriciones
    else:
        form = ComidaForm()
    
    return render(request, 'agregar_comidas.html', {'form': form})