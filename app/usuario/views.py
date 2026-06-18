from django.shortcuts import render, redirect
from .models import Usuario
from app.familiares.models import Familiar
from .forms import LoginForm
import logging
logger = logging.getLogger('auditoria')

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        codigo = form.cleaned_data['codigo']
        password = form.cleaned_data['password']
        try:
            user = Usuario.objects.get(codUsuario=codigo)
            if user.check_password(password):
                ip = request.META.get('REMOTE_ADDR')
                logger.info(f"Inicio de sesión exitoso: {user.codUsuario} desde IP {ip}")
                # GUARDAR SESIÓN (CLAVE)
                request.session['usuario'] = user.codUsuario
                
                if Familiar.objects.filter(usuario=user).exists():
                    return redirect('familiares:perfil')
                else:
                    return render(request, "usuario/login.html", {
                        "form": form,
                        "error": "Usuario sin tipo"
                    })

            else:
                return render(request, "usuario/login.html", {
                    "form": form,
                    "error": "Contraseña incorrecta"
                })

        except Usuario.DoesNotExist:
            return render(request, "usuario/login.html", { "form": form, "error": "El usuario no existe"})
    return render(request, "usuario/login.html", {"form": form})
def cambiar_password(request):
    cod_usuario = request.session.get('usuario')
    if not cod_usuario:
        return redirect('login')
    
    from .models import Usuario  # si ya está importado arriba, omite esta línea
    usuario = Usuario.objects.get(codUsuario=cod_usuario)
    error = None
    exito = None
    
    if request.method == 'POST':
        nueva = request.POST.get('nueva_password')
        confirmar = request.POST.get('confirmar_password')
        
        if nueva and nueva == confirmar:
            usuario.password = nueva   # el modelo lo hashea automáticamente
            usuario.save()
            logger.info(f"Usuario {usuario.codUsuario} cambió su contraseña")
            exito = "Contraseña cambiada exitosamente"
        else:
            error = "Las contraseñas no coinciden"
    
    return render(request, 'usuario/cambiar_password.html', {
        'error': error,
        'exito': exito,
    })