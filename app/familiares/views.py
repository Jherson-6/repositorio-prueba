from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.usuario.models import Usuario
from app.familiares.models import Familiar
import logging
logger = logging.getLogger('auditoria')

from .forms import(
    FamiliarCreacionForm, FamiliarEdicionForm
)
def perfil(request):
    cod_usuario = request.session.get('usuario')
    if not cod_usuario:
        return redirect('index') 
    try:
        familiar= Familiar.objects.select_related("usuario").get(usuario__codUsuario=cod_usuario)
    except Familiar.DoesNotExist:
        return redirect('index')

    return render(request, "familiares/perfil.html", {"familiar": familiar})


# ---------- Listado de estudiantes ----------

def gestion_familiares(request):
    familiar = Familiar.objects.select_related('usuario').all()
    
    context = {
        'familiar': familiar,
    }
    return render(request, 'familiares/gestion.html', context)

# ---------- Crear estudiante ----------
def crear_familiar(request):
    if request.method == 'POST':
        form = FamiliarCreacionForm(request.POST, request.FILES)
        if form.is_valid():
            familiar_creado = form.save()  # guardamos la instancia
            usuario_actual = request.session.get('usuario')
            logger.info(f"Usuario {usuario_actual} se creo al familiar {familiar_creado.codFamiliar}")
            messages.success(request, 'Familiar creado con éxito.')
            return redirect('familiares:gestion')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = FamiliarCreacionForm()
    return render(request, 'familiares/crear.html', {'form': form})

# ---------- Editar estudiante ----------

def editar_familiar(request, pk):
    familiar = get_object_or_404(Familiar, pk=pk)
    if request.method == 'POST':
        form = FamiliarEdicionForm(request.POST, request.FILES, instance=familiar)
        if form.is_valid():
            form.save()
            messages.success(request, 'Familiar actualizado correctamente.')
            return redirect('familiares:gestion')
    else:
        form = FamiliarEdicionForm(instance=familiar)
    return render(request, 'familiares/editar.html', {'form': form})

# ---------- Eliminar estudiante ----------
def eliminar_familiar(request, pk):
    familiar = get_object_or_404(Familiar, pk=pk)
    if request.method == 'POST':
        usuario = familiar.usuario
        familiar.delete()
        usuario.delete()  # Elimina también el usuario asociado
        messages.success(request, 'Familiar eliminado correctamente.')
        return redirect('familiares:gestion')
    return render(request, 'familiares/eliminar.html', {'familiar': familiar})
