import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import Rutina, EjercicioEnRutina, TipoRutina, Usuario
from .forms import RutinaForm, EjercicioEnRutinaForm, RutinaExistenteForm, TipoRutinaModelForm


def ver_rutinas(request):
    rutinas = Rutina.objects.all()  # Obtén todas las rutinas de la base de datos
    return render(request, 'rutinas.html', {'rutinas': rutinas})

@login_required
def dashboard_view(request):
    user = request.user
    return render(request, 'index.html', {'user': user})


def index(request):
    return render(request, 'rutinas/rutinas.html')  # Ruta específica a la plantilla de rutinas



@login_required
def lista_rutinas(request):
    """Vista principal que muestra la lista de rutinas del usuario."""
    context = {
        'rutinas': Rutina.objects.filter(usuario_creador=request.user, activa=True),
        'todas_rutinas': Rutina.objects.filter(activa=True),
        'tipos_rutina': TipoRutina.objects.all()
    }
    return render(request, 'lista_rutinas.html', context)

@login_required
@require_POST
def agregar_rutina_existente(request):
    """Permite al usuario agregar una rutina existente a su lista."""
    form = RutinaExistenteForm(request.POST)
    if form.is_valid():
        rutina_original = form.cleaned_data['rutina']
        
        # Crear una copia de la rutina para el usuario
        nueva_rutina = Rutina.objects.create(
            nombre=f"{rutina_original.nombre} (Copia)",
            tipo=rutina_original.tipo,
            descripcion=rutina_original.descripcion,
            nivel=rutina_original.nivel,
            duracion_estimada=rutina_original.duracion_estimada,
            calorias_estimadas=rutina_original.calorias_estimadas,
            usuario_creador=request.user
        )

        # Copiar los ejercicios de la rutina original
        for ejercicio in rutina_original.ejercicios.all():
            EjercicioEnRutina.objects.create(
                rutina=nueva_rutina,
                nombre_ejercicio=ejercicio.nombre_ejercicio,
                descripcion=ejercicio.descripcion,
                series=ejercicio.series,
                repeticiones=ejercicio.repeticiones,
                descanso=ejercicio.descanso,
                orden=ejercicio.orden,
                notas=ejercicio.notas
            )

        messages.success(request, 'Rutina agregada exitosamente.')
        return redirect('lista_rutinas')
    
    messages.error(request, 'Error al agregar la rutina.')
    return redirect('lista_rutinas')

@login_required
def crear_rutina(request):
    """Vista para crear una nueva rutina."""
    # Debug: Verificar tipos de rutina disponibles
    tipos_disponibles = TipoRutina.objects.all()
    print(f"Tipos de rutina disponibles: {list(tipos_disponibles)}")

    if request.method == 'POST':
        form = RutinaForm(request.POST, user=request.user)
        if form.is_valid():
            rutina = form.save()
            messages.success(request, 'Rutina creada exitosamente.')
            return redirect('lista_rutinas')
        else:
            print(f"Errores del formulario: {form.errors}")
            messages.error(request, 'Error al crear la rutina.')
    else:
        form = RutinaForm(user=request.user)

    context = {
        'form': form,
        'tipos_rutina': tipos_disponibles,  # Pasar explícitamente los tipos
    }
    
    return render(request, 'crear_rutina.html', context)

@login_required
def crear_ejercicio(request):
    """Vista para agregar un ejercicio a una rutina."""
    if request.method == 'POST':
        form = EjercicioEnRutinaForm(request.POST)
        if form.is_valid():
            ejercicio = form.save(commit=False)
            # Obtener la rutina seleccionada
            rutina_id = request.POST.get('rutina')
            rutina = get_object_or_404(Rutina, id=rutina_id, usuario_creador=request.user)
            
            # Establecer el orden del ejercicio
            ultimo_orden = rutina.ejercicios.count()
            ejercicio.rutina = rutina
            ejercicio.orden = ultimo_orden + 1
            ejercicio.save()
            
            messages.success(request, 'Ejercicio agregado exitosamente.')
            return redirect('lista_rutinas')
        else:
            messages.error(request, 'Error al agregar el ejercicio.')
    else:
        form = EjercicioEnRutinaForm()
    
    return render(request, 'crear_ejercicio.html', {'form': form})

@login_required
@require_POST
def agregar_ejercicio_rutina(request):
    """API endpoint para agregar un ejercicio específico a la rutina del usuario."""
    try:
        data = json.loads(request.body)
        ejercicio_id = data.get('ejercicio_id')
        ejercicio_original = get_object_or_404(EjercicioEnRutina, id=ejercicio_id)
        
        # Verificar si el usuario tiene una rutina activa o crear una nueva
        rutina_usuario = Rutina.objects.filter(
            usuario_creador=request.user,
            activa=True
        ).first()
        
        if not rutina_usuario:
            rutina_usuario = Rutina.objects.create(
                nombre="Mi Rutina Personalizada",
                tipo=ejercicio_original.rutina.tipo,
                descripcion="Rutina personalizada",
                nivel=ejercicio_original.rutina.nivel,
                usuario_creador=request.user
            )
        
        # Crear copia del ejercicio en la rutina del usuario
        ultimo_orden = rutina_usuario.ejercicios.count()
        nuevo_ejercicio = EjercicioEnRutina.objects.create(
            rutina=rutina_usuario,
            nombre_ejercicio=ejercicio_original.nombre_ejercicio,
            descripcion=ejercicio_original.descripcion,
            series=ejercicio_original.series,
            repeticiones=ejercicio_original.repeticiones,
            descanso=ejercicio_original.descanso,
            orden=ultimo_orden + 1,
            notas=ejercicio_original.notas
        )
        
        return JsonResponse({'success': True, 'message': 'Ejercicio agregado exitosamente'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def ver_ejercicios_rutina(request, rutina_id):
    """Vista para ver los ejercicios de una rutina específica."""
    rutina = get_object_or_404(Rutina, id=rutina_id)
    ejercicios = rutina.ejercicios.all().order_by('orden')
    return JsonResponse({
        'ejercicios': list(ejercicios.values(
            'id', 'nombre_ejercicio', 'series', 'repeticiones', 'descanso', 'notas'
        ))
    })

@login_required
def eliminar_ejercicio(request, ejercicio_id):
    """Vista para eliminar un ejercicio de una rutina."""
    ejercicio = get_object_or_404(EjercicioEnRutina, id=ejercicio_id)
    if ejercicio.rutina.usuario_creador != request.user:
        messages.error(request, 'No tienes permiso para eliminar este ejercicio.')
        return redirect('lista_rutinas')
    
    ejercicio.delete()
    messages.success(request, 'Ejercicio eliminado exitosamente.')
    return redirect('lista_rutinas')

@login_required
def actualizar_orden_ejercicios(request):
    """API endpoint para actualizar el orden de los ejercicios en una rutina."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ejercicios_orden = data.get('ejercicios', [])
            
            with transaction.atomic():
                for item in ejercicios_orden:
                    ejercicio = get_object_or_404(
                        EjercicioEnRutina,
                        id=item['id'],
                        rutina__usuario_creador=request.user
                    )
                    ejercicio.orden = item['orden']
                    ejercicio.save()
                    
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@login_required
def crear_tipo_rutina(request):
    if request.method == 'POST':
        form = TipoRutinaModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de rutina creado exitosamente.')
            return redirect('rutinas:index')
    else:
        form = TipoRutinaModelForm()
    
    context = {
        'form': form,
        # Aquí puedes agregar más contexto si lo necesitas
    }
    return render(request, 'rutinas.html', context)