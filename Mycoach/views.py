from pyexpat.errors import messages
from django.shortcuts import redirect, render
from Mysite.forms import ComidaForm
from rutinas.models import Nutricion, Usuario
def ver_usuarios(request):
    usuarios = Usuario.objects.all()  # Obtiene todos los usuarios
    return render(request, 'usuarios.html', {'usuarios': usuarios})  # Renderiza la plantilla


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


def registrar_usuario(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        contrasena = request.POST.get('contrasena')
        rol = request.POST.get('rol')
        sexo = request.POST.get('sexo')
        edad = request.POST.get('edad')
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')

        # Crear el usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            contrasena=contrasena,  # Asegúrate de encriptar la contraseña en un entorno real
            rol=rol,
            sexo=sexo,
            edad=edad,
            peso=peso,
            altura=altura,
            fecha_nacimiento=fecha_nacimiento
        )
        
        # Guardar el usuario en la base de datos
        nuevo_usuario.save()

        messages.success(request, 'Usuario registrado exitosamente.')
        return redirect('index')  # Redirigir a la página principal o a otra página

    return render(request, 'templates/registro_usuario.html')  # Mostrar el formulario si no es POST
