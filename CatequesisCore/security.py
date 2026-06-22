import os
import base64
import boto3
from botocore.exceptions import ClientError
from keycloak import KeycloakOpenID

class KeycloakManager:
    def __init__(self):
        # Asegurar que tomamos el valor del entorno y que no esté vacío
        self.server_url = os.environ.get('KEYCLOAK_URL') or 'http://localhost:8080'
        
        # Validación extra: si no tiene http:// o https://, algo anda mal en la config
        if self.server_url and not self.server_url.startswith(('http://', 'https://')):
            # Si parece una URL de Render o similar pero le falta el esquema
            if '.onrender.com' in self.server_url or 'localhost' in self.server_url:
                self.server_url = f"https://{self.server_url}" if 'onrender' in self.server_url else f"http://{self.server_url}"

        self.realm_name = os.environ.get('KC_REALM') or 'catequesis-realm'
        self.client_id = os.environ.get('KC_CLIENT_ID') or 'catequesis-app'
        self.client_secret = os.environ.get('KC_CLIENT_SECRET', '')
        
        try:
            self.keycloak_openid = KeycloakOpenID(
                server_url=self.server_url,
                client_id=self.client_id,
                realm_name=self.realm_name,
                client_secret_key=self.client_secret
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error initializing KeycloakOpenID with URL {self.server_url}: {e}")
            raise

    def get_login_url(self, redirect_uri):
        return self.keycloak_openid.auth_url(
            redirect_uri=redirect_uri,
            scope="openid profile email"
        )

    def get_token(self, code, redirect_uri):
        return self.keycloak_openid.token(
            grant_type='authorization_code',
            code=code,
            redirect_uri=redirect_uri
        )

    def get_user_info(self, token):
        return self.keycloak_openid.userinfo(token)

    def get_logout_url(self, redirect_uri):
        return f"{self.server_url}/realms/{self.realm_name}/protocol/openid-connect/logout?post_logout_redirect_uri={redirect_uri}&client_id={self.client_id}"

class KMSManager:
    def __init__(self):
        self.aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.region_name = os.environ.get('AWS_REGION_NAME', 'us-east-1')
        self.key_arn = os.environ.get('AWS_KMS_KEY_ARN')

        if self.aws_access_key and self.aws_secret_key:
            self.client = boto3.client(
                'kms',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.region_name
            )
        else:
            # Fallback local o IAM Role de EC2
            self.client = boto3.client('kms', region_name=self.region_name)

    def encrypt(self, plaintext, key_name=None):
        try:
            response = self.client.encrypt(
                KeyId=self.key_arn,
                Plaintext=plaintext.encode('utf-8')
            )
            ciphertext_blob = response['CiphertextBlob']
            return base64.b64encode(ciphertext_blob).decode('utf-8')
        except ClientError as e:
            print(f"[AWS KMS ERROR] Error al cifrar: {e.response['Error']['Message']}")
            return None
        except Exception as e:
            print(f"[AWS KMS ERROR] Error inesperado al cifrar: {e}")
            return None

    def decrypt(self, ciphertext_base64, key_name=None):
        try:
            ciphertext_blob = base64.b64decode(ciphertext_base64.encode('utf-8'))
            response = self.client.decrypt(
                CiphertextBlob=ciphertext_blob
            )
            return response['Plaintext'].decode('utf-8')
        except ClientError as e:
            print(f"[AWS KMS ERROR] Error al descifrar: {e.response['Error']['Message']}")
            return None
        except Exception as e:
            print(f"[AWS KMS ERROR] Error inesperado al descifrar: {e}")
            return None

kms_manager = KMSManager()
keycloak_manager = KeycloakManager()
