from django.shortcuts import  redirect, render

from Mysite.forms import ComidaForm


# Create your views here.
from rutinas.models import Nutricion






def index(request):
    # Recuperar todas las nutriciones
    comidas = Nutricion.objects.all()  # Aquí obtienes todos los registros de la tabla Nutricion
    return render(request, 'control_de_peso/index.html', {'nutriciones': comidas})


def ver_nutriciones(request):
    # Obtener todas las nutriciones ordenadas por nombre
    nutriciones = Nutricion.objects.all().order_by('nombre_comida')
    
    # Para debug - imprime en la consola
    print(f"Cantidad de nutriciones encontradas: {nutriciones.count()}")
    for nutricion in nutriciones:
        print(f"Nutrición: {nutricion.nombre_comida}, Calorías: {nutricion.calorias}")
    
    # Renderizar el template con los datos
    return render(request, 'ver_nutriciones.html', {
        'nutriciones': nutriciones
    })



def ver_nutricion(request):
    nutriciones = Nutricion.objects.all()
    return render(request, 'ver_nutriciones.html', {'nutriciones': nutriciones})



def agregar_comida(request):
    if request.method == 'POST':
        form = ComidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('controlpesos:ver_nutriciones')  # Redirigir a la lista después de guardar
    else:
        form = ComidaForm()
    
    return render(request, 'agregar_comidas.html', {'form': form})