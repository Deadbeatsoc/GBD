from django.shortcuts import  redirect, render

from Mysite.forms import ComidaForm


# Create your views here.
from .models import Nutricion






def index(request):
    # Recuperar todas las nutriciones
    comidas = Nutricion.objects.all()  # Aquí obtienes todos los registros de la tabla Nutricion
    return render(request, 'control_de_peso/index.html', {'nutriciones': comidas})





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
            return redirect('controlpesos:index')  # Redirige a la vista index de controlpesos
    else:
        form = ComidaForm()
    
    return render(request, 'agregar_comidas.html', {'form': form})