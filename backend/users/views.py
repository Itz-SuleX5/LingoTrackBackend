from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import jwt  # Si no lo tienes, instálalo con: pip install PyJWT
from .models import CustomUser
from .serializers import CustomUserSerializer


@api_view(['POST'])
def create_or_update_user(request):
    # 1. Obtener el token del header
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header or 'Bearer ' not in auth_header:
        return Response({"error": "Authorization header no encontrado o mal formateado"}, status=status.HTTP_401_UNAUTHORIZED)

    token = auth_header.split(' ')[1]

    try:
        # 2. Decodificar el token para obtener el auth0_id (el campo 'sub')
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        auth0_user_id = decoded_token.get('sub')

        if not auth0_user_id:
            return Response({"error": "No se pudo encontrar el 'sub' (user ID) en el token"}, status=status.HTTP_400_BAD_REQUEST)

    except jwt.DecodeError:
        return Response({"error": "Token inválido"}, status=status.HTTP_400_BAD_REQUEST)

    # 3. Usar el auth0_id para buscar o crear el usuario
    try:
        user = CustomUser.objects.get(auth0_id=auth0_user_id)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
    except CustomUser.DoesNotExist:
        data = request.data.copy()
        data['auth0_id'] = auth0_user_id
        serializer = CustomUserSerializer(data=data)

    # 4. Validar y guardar
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_profile(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header or 'Bearer ' not in auth_header:
        return Response({"error": "Authorization header no encontrado o mal formateado"}, status=status.HTTP_401_UNAUTHORIZED)

    token = auth_header.split(' ')[1]

    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        auth0_user_id = decoded_token.get('sub')
    except jwt.DecodeError:
        return Response({"error": "Token invalido"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = CustomUser.objects.get(auth0_id=auth0_user_id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_all_users(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_all_users(request):
    CustomUser.objects.all().delete()
    return Response({"message": "Todos los usuarios han sido eliminados."}, status=status.HTTP_200_OK)
