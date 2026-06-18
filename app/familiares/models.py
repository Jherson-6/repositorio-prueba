from django.db import models
from app.usuario.models import Usuario
# Create your models here.

class Familiar(models.Model):
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    parentesco = models.CharField(max_length=50)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    codFamiliar = models.CharField(primary_key=True, max_length=10)