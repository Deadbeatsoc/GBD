from pyexpat.errors import messages
from django.shortcuts import redirect, render
from Mysite.forms import AsignarPlanNutricionalForm, AsignarRutinaForm, ComidaForm, LoginForm, RegistroForm
from rutinas.models import Nutricion, PlanNutricional, Rutina, Usuario
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from rutinas.models import Usuario
from rutinas.models import ValoracionPersonal
from django.contrib.auth.decorators import login_required
from .forms import ValoracionPersonalForm
from django.contrib.auth.hashers import make_password, check_password



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
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            # Verificar que las contraseñas coincidan
            if form.cleaned_data['contrasena'] == form.cleaned_data['confirmar_contrasena']:
                usuario.contrasena = make_password(form.cleaned_data['contrasena'])
                usuario.save()
                messages.success(request, '¡Usuario registrado exitosamente!')
                return redirect('mycoach:login')
            else:
                messages.error(request, 'Las contraseñas no coinciden')
    else:
        form = RegistroForm()
    return render(request, 'registro_usuario.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            contrasena = form.cleaned_data['contrasena']
            try:
                usuario = Usuario.objects.get(email=email)
                if check_password(contrasena, usuario.contrasena):
                    request.session['usuario_id'] = usuario.id
                    return redirect('index')
                else:
                    messages.error(request, 'Contraseña incorrecta')
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuario no encontrado')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})



def cerrar_sesion(request):
    logout(request)
    return redirect('login')





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
def editar_nutricion(request, pk):
    # Obtener el objeto Nutricion o devolver un error 404 si no existe
    nutricion = get_object_or_404(Nutricion, pk=pk)
    
    if request.method == 'POST':
        # Pasar la instancia de Nutricion al formulario para editar
        form = ComidaForm(request.POST, instance=nutricion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información de nutrición actualizada exitosamente')
            # Redirigir a la vista de nutriciones (ajusta el nombre de la URL según tu configuración)
            return redirect('controlpesos:ver_nutriciones')
    else:
        form = ComidaForm(instance=nutricion)
    
    context = {
        'form': form,
        'titulo': 'Editar Información de Nutrición'
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



@login_required
def agregar_valoracion(request):
    if request.method == 'POST':
        form = ValoracionPersonalForm(request.POST)
        if form.is_valid():
            valoracion = form.save(commit=False)
            valoracion.usuario = request.user  # Asigna la valoración al usuario actual
            valoracion.save()
            messages.success(request, 'Valoración personal agregada exitosamente.')
            return redirect('mycoach:usuarios')  # Redirige a la página de información personal
    else:
        form = ValoracionPersonalForm()

    return render(request, 'editar_agregar_valoracion.html', {'form': form, 'titulo': 'Agregar Valoración Personal'})

@login_required
def editar_valoracion(request, pk):
    valoracion = get_object_or_404(ValoracionPersonal, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = ValoracionPersonalForm(request.POST, instance=valoracion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Valoración personal actualizada exitosamente.')
            return redirect('mycoach:usuarios')  # Redirige a la página de información personal
    else:
        form = ValoracionPersonalForm(instance=valoracion)

    return render(request, 'editar_agregar_valoracion.html', {'form': form, 'titulo': 'Editar Valoración Personal'})

@login_required
def ver_valoracion(request, pk):
    valoracion = get_object_or_404(ValoracionPersonal, pk=pk, usuario=request.user)

    return render(request, 'ver_valoracion.html', {
        'valoracion': valoracion,
        'titulo': 'Detalle de Valoración Personal'
    })
