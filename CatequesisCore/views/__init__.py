from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .auth_views import login_view, callback_view, logout_view
from .catequista_views import listar_catequistas, agregar_catequista, editar_catequista, eliminar_catequista, buscar_catequista, listar_datos_recibidos
from .estudiante_views import listar_estudiantes, agregar_estudiante, editar_estudiante, eliminar_estudiante, buscar_estudiante
from .grupo_views import listar_grupos
from .api_views import receive_textil_data

@login_required
def index(request):
    return render(request, 'index.html')

