from abc import ABC, abstractmethod
from typing import Optional, Dict
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ..security import keycloak_manager

class AuthStrategy(ABC):
    """Strategy interface for authentication mechanisms."""
    @abstractmethod
    def authenticate(self, request, credentials: Dict) -> Optional[User]:
        raise NotImplementedError()

class PasswordStrategy(AuthStrategy):
    """Authenticate using username/password via Django's `authenticate`."""
    def authenticate(self, request, credentials: Dict) -> Optional[User]:
        username = credentials.get('username')
        password = credentials.get('password')
        if username is None or password is None:
            return None
        return authenticate(request, username=username, password=password)

class KeycloakStrategy(AuthStrategy):
    """Autenticación mediante Keycloak (OIDC)."""
    def authenticate(self, request, credentials: Dict) -> Optional[User]:
        code = credentials.get('code')
        redirect_uri = credentials.get('redirect_uri')
        
        if not code or not redirect_uri:
            return None
            
        try:
            token_response = keycloak_manager.get_token(code, redirect_uri)
            access_token = token_response['access_token']
            
            try:
                user_info = keycloak_manager.get_user_info(access_token)
            except Exception:
                user_info = keycloak_manager.keycloak_openid.decode_token(access_token)
            
            username = user_info.get('preferred_username') or user_info.get('sub')
            email = user_info.get('email', '')
            first_name = user_info.get('given_name', '')
            last_name = user_info.get('family_name', '')
            
            user, created = User.objects.get_or_create(
                username=username, 
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name
                }
            )
            
            # Sincronizar roles de Keycloak (buscar en client roles y realm roles del Access Token decodificado)
            client_id = keycloak_manager.client_id
            
            try:
                # El access_token es un JWT que contiene los roles asignados por el Identity Provider
                decoded_token = keycloak_manager.keycloak_openid.decode_token(access_token)
            except Exception as de:
                print(f"[SECURITY WARNING] No se pudo decodificar el access_token con firma: {str(de)}. Intentando sin verificación de firma.")
                # Decodificar el token sin verificar firma como fallback (ya que lo obtuvimos directamente de Keycloak por HTTPS)
                import jwt
                decoded_token = jwt.decode(access_token, options={"verify_signature": False})
                
            client_roles = decoded_token.get('resource_access', {}).get(client_id, {}).get('roles', [])
            realm_roles = decoded_token.get('realm_access', {}).get('roles', [])
            all_roles = list(set(client_roles + realm_roles))
            
            # Convertir roles a minúsculas para evitar problemas de case sensitivity
            all_roles_lower = [r.lower() for r in all_roles]
            
            # LOGS DE SEGURIDAD (Se verán en la consola de Render)
            print(f"[SECURITY INFO] Intentando sincronizar roles para usuario: {username}")
            print(f"[SECURITY INFO] Client ID configurado: {client_id}")
            print(f"[SECURITY INFO] Roles de Cliente encontrados en JWT: {client_roles}")
            print(f"[SECURITY INFO] Roles de Realm encontrados en JWT: {realm_roles}")
            print(f"[SECURITY INFO] Todos los roles combinados: {all_roles}")
            
            if hasattr(user, 'profile'):
                profile = user.profile
                if 'admin' in all_roles_lower:
                    profile.role = 'admin'
                    print("[SECURITY INFO] Rol asignado en Django: admin")
                elif 'catequista' in all_roles_lower:
                    profile.role = 'catequista'
                    print("[SECURITY INFO] Rol asignado en Django: catequista")
                else:
                    profile.role = 'visitante'
                    print("[SECURITY INFO] Rol asignado en Django: visitante (Sin Permisos)")
                profile.save()
            
            return user
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en KeycloakStrategy: {str(e)}")
            return None
