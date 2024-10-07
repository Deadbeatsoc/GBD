from django.shortcuts import redirect, render
from .forms import UsuarioForm


def index(request):
    return render(request, 'index.html')



def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el usuario en la base de datos
            return redirect('homepage')  # Redirige a la página principal o a donde desees
    else:
        form = UsuarioForm()
    return render(request, 'crear_usuario.html', {'form': form})