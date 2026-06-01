from django.shortcuts import render
from .auth_views import login_view, callback_view, logout_view
from .catequista_views import listar_catequistas, agregar_catequista, editar_catequista, eliminar_catequista, buscar_catequista
from .estudiante_views import listar_estudiantes, agregar_estudiante, editar_estudiante, eliminar_estudiante, buscar_estudiante

def index(request):
    return render(request, 'index.html')
