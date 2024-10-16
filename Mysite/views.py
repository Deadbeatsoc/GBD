from django.shortcuts import redirect, render

from rutinas.models import Usuario
from .forms import UsuarioForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout





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




def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Verifica si el usuario existe con el correo y contraseña proporcionados
        try:
            user = Usuario.objects.get(email=email, contrasena=password)
            # Si el usuario es válido, inicias sesión
            if user:
                # Aquí puedes usar 'login' si estás usando el sistema de autenticación predeterminado de Django
                messages.success(request, f'Bienvenido, {user.nombre}!')
                return redirect('index')  # Redirige a la página principal
        except Usuario.DoesNotExist:
            # Si no coincide, muestra un mensaje de error
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'registration/login.html')
