from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login, logout
from ..security import keycloak_manager
from ..services.auth_strategies import KeycloakStrategy

def login_view(request):
    redirect_uri = request.build_absolute_uri(reverse('callback'))
    # Asegurar 127.0.0.1 para coincidir con Keycloak local si es necesario
    if 'localhost' in redirect_uri:
        redirect_uri = redirect_uri.replace('localhost', '127.0.0.1')
    return redirect(keycloak_manager.get_login_url(redirect_uri))

def callback_view(request):
    code = request.GET.get('code')
    if not code:
        return render(request, 'error.html', {'message': 'No code provided'})
    
    redirect_uri = request.build_absolute_uri(reverse('callback'))
    if 'localhost' in redirect_uri:
        redirect_uri = redirect_uri.replace('localhost', '127.0.0.1')
    
    strategy = KeycloakStrategy()
    user = strategy.authenticate(request, {'code': code, 'redirect_uri': redirect_uri})
    
    if user:
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'error.html', {'message': 'Error en la autenticación'})

def logout_view(request):
    logout(request)
    redirect_uri = request.build_absolute_uri(reverse('index'))
    return redirect(keycloak_manager.get_logout_url(redirect_uri))
