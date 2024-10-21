from django.shortcuts import redirect, render
from Mysite.forms import EjercicioForm
from rutinas.forms import RutinaForm
from .models import Ejercicio, Rutina

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



def agregar_rutina(request):
    if request.method == 'POST':
        form = RutinaForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar la nueva rutina en la base de datos
            return redirect('rutinas')  # Redirige a la página de rutinas después de guardar
    else:
        form = RutinaForm()
    
    return render(request, 'agregar_rutina.html', {'form': form})



def agregar_ejercicio(request):
    if request.method == 'POST':
        form = EjercicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_ejercicios')  # Redirigir a la página que lista los ejercicios
    else:
        form = EjercicioForm()
    
    return render(request, 'agregar_ejercicio.html', {'form': form})


def ver_ejercicios(request):
    ejercicios = Ejercicio.objects.all()
    return render(request, 'ver_ejercicios.html', {'ejercicios': ejercicios})