from django.shortcuts import redirect, render
from rutinas.forms import RutinaForm
from rutinas.models import Ejercicio, Nutricion, Usuario   
from .forms import  ComidaForm, EjercicioForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout





def agregar_comida(request):
    if request.method == 'POST':
        form = ComidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_nutriciones')  # Redirigir a la lista de nutriciones
    else:
        form = ComidaForm()
    
    return render(request, 'agregar_comidas.html', {'form': form})



def ver_nutriciones(request):
    nutriciones = Nutricion.objects.all()
    return render(request, 'ver_nutriciones.html', {'nutriciones': nutriciones})



def ver_nutricion(request):
    nutriciones = Nutricion.objects.all()
    return render(request, 'ver_nutriciones.html', {'nutriciones': nutriciones})


def index(request):
    user = None
    if request.user.is_authenticated:
        user = request.user  # Obtener el usuario autenticado
    return render(request, 'index.html', {'user': user})

def logout_view(request):
    auth_logout(request)
    return redirect('login')


def registrar_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        contrasena = request.POST.get('contrasena')
        rol = request.POST.get('rol')
        edad = request.POST.get('edad')
        sexo = request.POST.get('sexo')
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')

        # Crear un nuevo usuario
        usuario = Usuario(
            nombre=nombre,
            email=email,
            contrasena=contrasena,  # Considera usar un hash para la contraseña
            rol=rol,
            edad=edad,
            sexo=sexo,
            peso=peso,
            altura=altura,
            fecha_nacimiento=fecha_nacimiento
        )

        
        # Guardar el usuario en la base de datos
        usuario.save()
        
        messages.success(request, 'Usuario creado exitosamente.')
        return redirect('index')  # Redirigir a la página principal

    return render(request, 'registro_usuario.html')  # Muestra el formulario de registro









