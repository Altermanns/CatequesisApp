from django.shortcuts import render, redirect
from ..services.catequista_service import CatequistaService
from ..decorators import catequista_required, admin_required

service = CatequistaService()

@catequista_required
def listar_catequistas(request):
    lista = service.obtener_todos()
    return render(request, 'catequistas.html', {'catequistas': lista})

@admin_required
def agregar_catequista(request):
    if request.method == 'POST':
        data = {
            "_id": request.POST['idCatequista'],
            "nombre": request.POST['nombre'],
            "apellido": request.POST['apellido'],
            "email": request.POST['email'],
            "telefono": request.POST['telefono'],
            "nivel": request.POST['nivel'],
            "estado": "Activo",
            "grupos_asignados": []
        }
        service.crear_catequista(data)
        return redirect('listar_catequistas')
    return redirect('listar_catequistas')

@admin_required
def editar_catequista(request, id):
    if request.method == 'POST':
        data = {
            "nombre": request.POST['nombre'],
            "apellido": request.POST['apellido'],
            "nivel": request.POST['nivel'],
            "email": request.POST['email'],
            "telefono": request.POST['telefono']
        }
        service.actualizar_catequista(id, data)
        return redirect('listar_catequistas')
    
    catequista = service.obtener_por_id(id)
    return render(request, 'editar_catequista.html', {'catequista': catequista})

@admin_required
def eliminar_catequista(request, id):
    service.eliminar_catequista(id)
    return redirect('listar_catequistas')

@catequista_required
def buscar_catequista(request):
    termino = request.GET.get('termino', '')
    resultados = service.buscar_por_nombre(termino)
    return render(request, 'catequistas.html', {'catequistas': resultados})
