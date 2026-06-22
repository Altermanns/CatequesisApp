from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('callback/', views.callback_view, name='callback'),
    path('logout/', views.logout_view, name='logout'),
    
    # Catequistas
    path('catequistas/', views.listar_catequistas, name='listar_catequistas'),
    path('catequistas/agregar/', views.agregar_catequista, name='agregar_catequista'),
    path('catequistas/editar/<str:id>/', views.editar_catequista, name='editar_catequista'),
    path('catequistas/eliminar/<str:id>/', views.eliminar_catequista, name='eliminar_catequista'),
    path('catequistas/buscar/', views.buscar_catequista, name='buscar_catequista'),
    
    # Estudiantes
    path('estudiantes/', views.listar_estudiantes, name='listar_estudiantes'),
    path('estudiantes/agregar/', views.agregar_estudiante, name='agregar_estudiante'),
    path('estudiantes/editar/<str:id>/', views.editar_estudiante, name='editar_estudiante'),
    path('estudiantes/eliminar/<str:id>/', views.eliminar_estudiante, name='eliminar_estudiante'),
    path('estudiantes/buscar/', views.buscar_estudiante, name='buscar_estudiante'),
    
    # Grupos
    path('grupos/', views.listar_grupos, name='listar_grupos'),
    
    # Datos Recibidos de TextilApp via KMS
    path('datos-recibidos/', views.listar_datos_recibidos, name='listar_datos_recibidos'),
    
    # API Integration (KMS Secure Communication)
    path('api/v1/sync-textil/', views.receive_textil_data, name='receive_textil_data'),
]
