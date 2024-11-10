from django.utils import timezone  # Asegúrate de importar esto
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from Mysite.forms import AsignarPlanNutricionalForm, AsignarRutinaForm, ComidaForm
from rutinas.models import Nutricion, PlanNutricional, Rutina, Usuario
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User  # Importa el modelo de usuario predeterminado de Django
from rutinas.models import Usuario
from rutinas.models import ValoracionPersonal
from Mycoach.forms import ValoracionForm
from django.contrib.auth.decorators import login_required



def index(request):
    user = None
    if request.user.is_authenticated:
        user = request.user  # Obtener el usuario autenticado
    return render(request, 'index.html', {'user': user})



def mi_informacion(request):
    usuario = request.user  # Obtener el usuario autenticado
    try:
        info_usuario = Usuario.objects.get(id=usuario.id)
    except Usuario.DoesNotExist:
        return redirect('mycoach:index')  # Redirigir si no encuentra el usuario

    # Cargar las valoraciones del usuario
    valoraciones = ValoracionPersonal.objects.filter(id=usuario.id)

    context = {
        'info_usuario': info_usuario,
        'valoraciones': valoraciones
    }
    return render(request, 'usuarios.html', context)

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

    return render(request, 'registro_usuario.html')  # Mostrar el formulario si no es POST


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Verifica si el usuario existe en la base de datos
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    login(request, user)  # Inicia sesión si la contraseña es correcta
                    return redirect('index')  # Redirige a la página principal o la que prefieras
                else:
                    error_message = "Contraseña incorrecta."
            except User.DoesNotExist:
                error_message = "El usuario no existe."

            return render(request, 'registration/login.html', {'form': form, 'error': error_message})
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})



def cerrar_sesion(request):
    logout(request)
    return redirect('login')



def agregar_valoracion(request):
    today = timezone.now().date()  # Obtiene la fecha actual
    if request.method == 'POST':
        form = ValoracionForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirige o muestra un mensaje de éxito
    else:
        form = ValoracionForm(initial={'fecha_valoracion': today})  # Establece la fecha de hoy como predeterminada

    return render(request, 'agregar_valoracion.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rutinas.models import Rutina, PlanNutricional, Usuario
from  Mysite.forms import AsignarRutinaForm, AsignarPlanNutricionalForm

# Vistas para Rutinas
@login_required
def lista_rutinas(request):
    rutinas = Rutina.objects.all()
    context = {
        'rutinas': rutinas,
        'titulo': 'Listado de Rutinas'
    }
    return render(request, 'rutinas/rutinas.html', context)






@login_required
def asignar_rutina(request):
    if request.method == 'POST':
        form = AsignarRutinaForm(request.POST)
        if form.is_valid():
            rutina = form.save()
            messages.success(request, 'Rutina asignada exitosamente')
            return redirect('rutinas')
    else:
        form = AsignarRutinaForm()
    
    context = {
        'form': form,
        'titulo': 'Asignar Nueva Rutina'
    }
    return render(request, 'asignar_rutinas.html', context)

@login_required
def editar_rutina(request, pk):
    rutina = get_object_or_404(Rutina, pk=pk)
    if request.method == 'POST':
        form = AsignarRutinaForm(request.POST, instance=rutina)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rutina actualizada exitosamente')
            return redirect('rutinas')
    else:
        form = AsignarRutinaForm(instance=rutina)
    
    context = {
        'form': form,
        'titulo': 'Editar Rutina'
    }
    return render(request, 'asignar_rutinas.html', context)

@login_required
def eliminar_rutina(request, pk):
    rutina = get_object_or_404(Rutina, pk=pk)
    if request.method == 'POST':
        rutina.delete()
        messages.success(request, 'Rutina eliminada exitosamente')
        return redirect('rutinas')
    return render(request, 'confirmar_eliminar.html', {'objeto': rutina})

# Vistas para Planes Nutricionales
@login_required
def lista_planes_nutricionales(request):
    planes = PlanNutricional.objects.all()
    context = {
        'planes': planes,
        'titulo': 'Listado de Planes Nutricionales'
    }
    return render(request, 'lista_planes.html', context)

@login_required
def asignar_plan_nutricional(request):
    if request.method == 'POST':
        form = AsignarPlanNutricionalForm(request.POST)
        if form.is_valid():
            plan = form.save()
            messages.success(request, 'Plan nutricional asignado exitosamente')
            return redirect('ver_nutriciones')
    else:
        form = AsignarPlanNutricionalForm()
    
    context = {
        'form': form,
        'titulo': 'Asignar Nuevo Plan Nutricional'
    }
    return render(request,'asignar_plan_nutricional.html', context)

@login_required
def editar_plan_nutricional(request, pk):
    plan = get_object_or_404(PlanNutricional, pk=pk)
    if request.method == 'POST':
        form = AsignarPlanNutricionalForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plan nutricional actualizado exitosamente')
            return redirect('ver_nutriciones')
    else:
        form = AsignarPlanNutricionalForm(instance=plan)
    
    context = {
        'form': form,
        'titulo': 'Editar Plan Nutricional'
    }
    return render(request, 'asignar_plan.html', context)

@login_required
def eliminar_plan_nutricional(request, pk):
    plan = get_object_or_404(PlanNutricional, pk=pk)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Plan nutricional eliminado exitosamente')
        return redirect('lista_planes_nutricionales')
    return render(request, 'confirmar_eliminar.html', {'objeto': plan})







@login_required
def eliminar_nutricion(request, pk):
    # Obtener el objeto de Nutricion o devolver un error 404 si no existe
    nutricion = get_object_or_404(Nutricion, pk=pk)
    
    if request.method == 'POST':
        # Eliminar el objeto si la solicitud es POST
        nutricion.delete()
        messages.success(request, 'Elemento de nutrición eliminado exitosamente')
        # Redirigir a la lista de nutriciones después de la eliminación
        return redirect('controlpesos:ver_nutriciones')
    
    # Mostrar una confirmación de eliminación si la solicitud es GET
    return render(request, 'confirmar_eliminar.html', {'objeto': nutricion})
