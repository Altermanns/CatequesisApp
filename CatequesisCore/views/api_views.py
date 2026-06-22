import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..security import kms_manager
from ..decorators import require_client_credentials

@csrf_exempt
@require_client_credentials
def receive_textil_data(request):
    """
    API endpoint that receives encrypted data from TextilApp,
    decrypts it using AWS KMS, and processes the payload.
    """
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed. Use POST."}, status=405)
    
    try:
        data = json.loads(request.body)
        ciphertext = data.get('ciphertext')
        
        if not ciphertext:
            return JsonResponse({"error": "Bad Request: Missing 'ciphertext' parameter"}, status=400)
        
        # 1. Decrypt with AWS KMS
        plaintext = kms_manager.decrypt(ciphertext)
        
        if not plaintext:
            return JsonResponse({"error": "Internal Error: Decryption failed on KMS"}, status=500)
        
        # 2. Parse the decrypted JSON
        payload = json.loads(plaintext)
        
        # 3. Log or process the payload
        print(f"[SECURITY INFO] Decrypted payload successfully: {payload}")
        
        # We can store the sync status or respond with a successful signature
        return JsonResponse({
            "status": "success",
            "message": "Data decrypted and processed successfully",
            "received_keys": list(payload.keys())
        })
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Bad Request: Malformed JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)
