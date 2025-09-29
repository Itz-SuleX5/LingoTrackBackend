import jwt
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from functools import wraps

def get_auth0_public_key():
    url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    response = requests.get(url)
    return response.json()

def validate_auth0_token(token):
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded, None
    except Exception as e:
        return None, f"Error validando token: {str(e)}"

def auth0_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or 'Bearer ' not in auth_header:
            return Response(
                {"error": "Authorization header requerido"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token = auth_header.split(' ')[1]
        decoded_token, error = validate_auth0_token(token)

        if error:
            return Response(
                {"error": error},
                status=status.HTTP_401_UNAUTHORIZED
            )

        request.auth0_user = decoded_token
        return f(request, *args, **kwargs)

    return decorated_function
