from django.shortcuts import render, redirect
from ..services.repositories import GrupoRepository
from ..decorators import catequista_required

service = GrupoRepository()

@catequista_required
def listar_grupos(request):
    lista = service.get_all()
    return render(request, 'grupos.html', {'grupos': lista})
