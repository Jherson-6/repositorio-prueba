from django.urls import path, include
from . import views
app_name = 'familiares'

urlpatterns = [
    path('', views.perfil, name='perfil'),
    # Gestión de familiares(nuevo)
    path('gestionFamiliar/', views.gestion_familiares, name='gestion'),
    path('gestion-familiares/editar/<int:pk>/', views.editar_familiar, name='editar'),
    path('gestion-familiares/eliminar/<int:pk>/', views.eliminar_familiar, name='eliminar'),
    path('crear-nuevoFamiliar/', views.crear_familiar, name='crear'),

]
