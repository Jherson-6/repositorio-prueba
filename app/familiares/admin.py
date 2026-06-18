from django.contrib.auth.hashers import make_password
from django.contrib import admin
from .models import Familiar

@admin.register(Familiar)
class FamiliarAdmin(admin.ModelAdmin):
    list_display = ('codFamiliar', 'usuario', 'nombre', 'apellido_paterno', 'apellido_materno', 'parentesco')
