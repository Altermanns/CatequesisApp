from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

def role_required(role):
    """
    Decorator to require a specific role in Catequesis.
    Usage: @role_required('admin') or @role_required('catequista')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, 'profile'):
                messages.error(request, 'Tu usuario no tiene un perfil asignado.')
                return redirect('index')
            
            if request.user.profile.role != role and request.user.profile.role != 'admin':
                messages.error(request, f'No tienes permisos para acceder a esta página. Se requiere rol: {role}')
                return redirect('index')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def admin_required(view_func):
    """Decorator to require admin role."""
    return role_required('admin')(view_func)

def catequista_required(view_func):
    """Decorator to require catequista role (or admin)."""
    return role_required('catequista')(view_func)

def require_client_credentials(view_func):
    """
    Decorator to validate Keycloak client credentials token (JWT) from the Authorization header.
    """
    from django.http import JsonResponse
    from .security import keycloak_manager

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({"error": "Unauthorized: Missing or malformed Authorization header"}, status=401)
        
        token = auth_header.split(' ')[1]
        try:
            # Validamos el token consultando al introspect endpoint de Keycloak
            introspection = keycloak_manager.keycloak_openid.introspect(token)
            if not introspection.get('active'):
                return JsonResponse({"error": "Unauthorized: Token is inactive or expired"}, status=401)
        except Exception as e:
            return JsonResponse({"error": f"Unauthorized: Token validation failed: {str(e)}"}, status=401)
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view
