from pyexpat.errors import messages
from django.shortcuts import redirect, render
from Mysite.forms import  ComidaForm, EjercicioForm
from rutinas.models import Nutricion, PlanNutricional, Rutina
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from rutinas.models import ValoracionPersonal
from django.contrib.auth.decorators import login_required
from .forms import ValoracionPersonalForm
from django.contrib.auth import authenticate, login
from rutinas.models import User




def index(request):
    user = None
    if request.user.is_authenticated:
        user = request.user  # Obtener el usuario autenticado
    return render(request, 'index.html', {'user': user})



def mi_informacion(request):
    usuario = request.user  # Obtener el usuario autenticado
    try:
        info_usuario = User.objects.get(id=usuario.id)  
    except User.DoesNotExist:
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




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm



def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registro_usuario.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = ''
    return render(request, 'registration/login.html', {'error_message': error_message})

def cerrar_sesion(request):
    logout(request)
    return redirect('login')





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rutinas.models import Rutina, PlanNutricional

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
def editar_rutina(request, pk):
    rutina = get_object_or_404(Rutina, pk=pk)
    if request.method == 'POST':
        form = EjercicioForm(request.POST, instance=rutina)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rutina actualizada exitosamente')
            return redirect('rutinas')
    else:
        form = EjercicioForm(instance=rutina)
    
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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta, date
from rutinas.models import ValoracionPersonal, User
from .forms import ValoracionPersonalForm

@login_required
def valoraciones_view(request):
    """Vista principal que muestra el dashboard de valoraciones"""
    # Obtener el período del filtro
    periodo = request.GET.get('periodo', None)
    
    # Obtener fecha actual
    fecha_actual = timezone.now().date()
    
    # Aplicar filtros según el período seleccionado
    if periodo == 'semana':
        fecha_inicio = fecha_actual - timedelta(days=7)
        valoraciones = ValoracionPersonal.objects.filter(
            usuario=request.user,
            fecha_valoracion__gte=fecha_inicio
        )
    elif periodo == 'mes':
        fecha_inicio = fecha_actual - timedelta(days=30)
        valoraciones = ValoracionPersonal.objects.filter(
            usuario=request.user,
            fecha_valoracion__gte=fecha_inicio
        )
    else:
        # Por defecto mostrar las últimas 5 valoraciones
        valoraciones = ValoracionPersonal.objects.filter(
            usuario=request.user
        )[:5]

    # Obtener la última valoración para mostrar IMC actual
    ultima_valoracion = ValoracionPersonal.objects.filter(
        usuario=request.user
    ).first()

    # Obtener información del usuario
    info_usuario = {
        'Nombre': f"{request.user.first_name} {request.user.last_name}",
        'Email': request.user.email,
        'Edad': calcular_edad(request.user.fecha_nacimiento) if hasattr(request.user, 'fecha_nacimiento') else None,
        'PesoActual': ultima_valoracion.masa_corporal if ultima_valoracion else None,
        'AlturaActual': request.user.altura_actual if hasattr(request.user, 'altura_actual') else None,
    }

    context = {
        'valoraciones': valoraciones,
        'info_usuario': info_usuario,
        'ultima_valoracion': ultima_valoracion,
    }
    
    return render(request, 'ver_valoracion.html', context)

@login_required
def agregar_valoracion(request):
    """Vista para agregar una nueva valoración"""
    if request.method == 'POST':
        form = ValoracionPersonalForm(request.POST)
        if form.is_valid():
            valoracion = form.save(commit=False)
            valoracion.usuario = request.user
            
            # Verificar si ya existe una valoración para esta fecha
            if ValoracionPersonal.objects.filter(
                usuario=request.user,
                fecha_valoracion=valoracion.fecha_valoracion
            ).exists():
                messages.error(request, 'Ya existe una valoración para esta fecha.')
                return render(request, 'agregar_valoracion.html', {'form': form})
            
            valoracion.save()
            messages.success(request, 'Valoración agregada exitosamente.')
            return redirect('mycoach:ver_valoraciones')
    else:
        # Prellenar la fecha con la fecha actual
        initial_data = {'fecha_valoracion': date.today()}
        form = ValoracionPersonalForm(initial=initial_data)
    
    return render(request, 'agregar_valoracion.html', {'form': form})

@login_required
def editar_valoracion(request, valoracion_id):
    """Vista para editar una valoración existente"""
    valoracion = get_object_or_404(ValoracionPersonal, id=valoracion_id, usuario=request.user)
    
    if request.method == 'POST':
        form = ValoracionPersonalForm(request.POST, instance=valoracion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Valoración actualizada exitosamente.')
            return redirect('mycoach:valoraciones')
    else:
        form = ValoracionPersonalForm(instance=valoracion)
    
    return render(request, 'editar_valoracion.html', {
        'form': form,
        'valoracion': valoracion
    })

@login_required
def ver_valoraciones(request, valoracion_id):
    """Vista para ver el detalle de una valoración"""
    valoracion = get_object_or_404(ValoracionPersonal, id=valoracion_id, usuario=request.user)
    
    # Obtener la valoración anterior para comparar
    valoracion_anterior = ValoracionPersonal.objects.filter(
        usuario=request.user,
        fecha_valoracion__lt=valoracion.fecha_valoracion
    ).first()

    context = {
        'valoracion': valoracion,
        'valoracion_anterior': valoracion_anterior,
        'imc': valoracion.calcular_imc(),
        'estado_imc': valoracion.get_estado_imc(),
    }
    
    return render(request, 'ver_valoracion.html', context)

@login_required
def historial_valoraciones(request):
    """Vista para ver el historial completo de valoraciones"""
    # Configurar filtros
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    valoraciones = ValoracionPersonal.objects.filter(usuario=request.user)
    
    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            valoraciones = valoraciones.filter(
                fecha_valoracion__range=[fecha_inicio, fecha_fin]
            )
        except ValueError:
            messages.error(request, 'Formato de fecha inválido')
    
    context = {
        'valoraciones': valoraciones,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    
    return render(request, 'historial_valoraciones.html', context)

def calcular_edad(fecha_nacimiento):
    """Función auxiliar para calcular la edad"""
    if not fecha_nacimiento:
        return None
    today = timezone.now().date()
    age = today.year - fecha_nacimiento.year
    if today.month < fecha_nacimiento.month or (
        today.month == fecha_nacimiento.month and 
        today.day < fecha_nacimiento.day
    ):
        age -= 1
    return age