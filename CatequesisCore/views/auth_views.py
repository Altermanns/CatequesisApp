import os
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login, logout
from ..security import keycloak_manager
from ..services.auth_strategies import KeycloakStrategy

def login_view(request):
    # Intentar obtener la URL base desde el entorno, de lo contrario usar la de la petición
    app_url = os.environ.get('APP_URL')
    if app_url:
        redirect_uri = f"{app_url.rstrip('/')}{reverse('callback')}"
    else:
        redirect_uri = request.build_absolute_uri(reverse('callback'))
    
    # Forzar HTTPS si estamos en producción (no local)
    if not request.get_host().startswith('127.0.0.1') and not request.get_host().startswith('localhost'):
        if request.headers.get('X-Forwarded-Proto') == 'https' or not request.is_secure():
            # Si estamos en Render o similar, a menudo necesitamos forzar https
            redirect_uri = redirect_uri.replace('http://', 'https://')
    
    print(f"DEBUG: Keycloak Redirect URI: {redirect_uri}")
    return redirect(keycloak_manager.get_login_url(redirect_uri))

def callback_view(request):
    code = request.GET.get('code')
    if not code:
        return render(request, 'error.html', {'message': 'No code provided'})
    
    app_url = os.environ.get('APP_URL')
    if app_url:
        redirect_uri = f"{app_url.rstrip('/')}{reverse('callback')}"
    else:
        redirect_uri = request.build_absolute_uri(reverse('callback'))
        
    if not request.get_host().startswith('127.0.0.1') and not request.get_host().startswith('localhost'):
        if request.headers.get('X-Forwarded-Proto') == 'https' or not request.is_secure():
            redirect_uri = redirect_uri.replace('http://', 'https://')
    
    print(f"DEBUG: Callback Redirect URI: {redirect_uri}")
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
