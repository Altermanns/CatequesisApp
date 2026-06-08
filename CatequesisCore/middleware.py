from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
import os

class SilentSSOMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Si el usuario ya está autenticado en Django, no hacer nada
        if request.user.is_authenticated:
            return self.get_response(request)

        # 2. Evitar bucles de redirección en rutas de auth
        path = request.path
        exempt_paths = [
            reverse('login'),
            reverse('callback'),
            reverse('logout'),
            '/admin/',
            '/static/',
        ]
        
        if any(path.startswith(p) for p in exempt_paths):
            return self.get_response(request)

        # 3. Solo intentar Silent SSO en la página de inicio o si el usuario intenta acceder a algo
        # Para evitar molestar al usuario, podemos usar un parámetro en la sesión para intentarlo solo una vez
        if not request.session.get('sso_checked', False):
            request.session['sso_checked'] = True
            
            # Construir la URL de login que redirigirá de vuelta al callback
            redirect_uri = request.build_absolute_uri(reverse('callback'))
            if 'localhost' in redirect_uri and os.environ.get('DJANGO_SETTINGS_MODULE') == 'CatequesisDjango.settings.development':
                redirect_uri = redirect_uri.replace('localhost', '127.0.0.1')
            
            # En producción (Render), forzar HTTPS
            if not request.get_host().startswith('127.0.0.1') and not request.get_host().startswith('localhost'):
                redirect_uri = redirect_uri.replace('http://', 'https://')

            from .security import keycloak_manager
            # El login_url de Keycloak por defecto intentará autenticar
            # Si el usuario ya tiene sesión en el navegador, Keycloak lo devolverá al callback de inmediato
            return redirect(keycloak_manager.get_login_url(redirect_uri))

        return self.get_response(request)
