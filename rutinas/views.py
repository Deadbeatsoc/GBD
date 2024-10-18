from django.shortcuts import redirect, render
from rutinas.forms import RutinaForm
from .models import Rutina

def ver_rutinas(request):
    rutinas = Rutina.objects.all()  # Obtén todas las rutinas de la base de datos
    return render(request, 'rutinas.html', {'rutinas': rutinas})



def index(request):
    return render(request, 'rutinas/rutinas.html')  # Ruta específica a la plantilla de rutinas

def agregar_rutina(request):
    if request.method == 'POST':
        form = RutinaForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar la nueva rutina en la base de datos
            return redirect('rutinas')  # Redirige a la página de rutinas después de guardar
    else:
        form = RutinaForm()
    
    return render(request, 'agregar_rutina.html', {'form': form})