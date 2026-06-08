from django.shortcuts import render, redirect
from ..services.estudiante_service import EstudianteService
from ..decorators import catequista_required, admin_required

service = EstudianteService()

@catequista_required
def listar_estudiantes(request):
    lista = service.obtener_todos()
    sacramentos = service.obtener_sacramentos()
    return render(request, 'estudiantes.html', {'estudiantes': lista, 'sacramentos': sacramentos})

@catequista_required
def agregar_estudiante(request):
    if request.method == 'POST':
        sacramentos_faltantes = request.POST.getlist('sacramentos')
        data = {
            "_id": request.POST['idEstudiante'],
            "nombre": request.POST['nombre'],
            "apellido": request.POST['apellido'],
            "edad": int(request.POST['edad']),
            "estado": "Activo",
            "grupo_id": request.POST['grupoId'],
            "sacramentos": sacramentos_faltantes,
            "padres": [{
                "nombre": request.POST['nombrePadre'],
                "telefono": request.POST['telefonoPadre'],
                "email": request.POST['emailPadre']
            }]
        }
        service.crear_estudiante(data)
        return redirect('listar_estudiantes')
    return redirect('listar_estudiantes')

@catequista_required
def editar_estudiante(request, id):
    if request.method == 'POST':
        data = {
            "nombre": request.POST['nombre'],
            "apellido": request.POST['apellido'],
            "edad": int(request.POST['edad']),
            "grupo_id": request.POST['grupoId'],
            "sacramentos": request.POST.getlist('sacramentos'),
            "padres": [{
                "nombre": request.POST['nombrePadre'],
                "telefono": request.POST['telefonoPadre'],
                "email": request.POST['emailPadre']
            }]
        }
        service.actualizar_estudiante(id, data)
        return redirect('listar_estudiantes')
    
    estudiante = service.obtener_por_id(id)
    sacramentos = service.obtener_sacramentos()
    return render(request, 'editar_estudiante.html', {'estudiante': estudiante, 'sacramentos': sacramentos})

@admin_required
def eliminar_estudiante(request, id):
    service.eliminar_estudiante(id)
    return redirect('listar_estudiantes')

@catequista_required
def buscar_estudiante(request):
    termino = request.GET.get('termino', '')
    resultados = service.buscar_por_nombre(termino)
    sacramentos = service.obtener_sacramentos()
    return render(request, 'estudiantes.html', {'estudiantes': resultados, 'sacramentos': sacramentos})
