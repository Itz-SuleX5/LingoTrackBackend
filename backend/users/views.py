from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer
from utils.auth0_utils import auth0_required

@api_view(['POST'])
@authentication_classes([])  # ← Desactiva autenticación DRF
@permission_classes([AllowAny])
@auth0_required
def create_or_update_user(request):
    # Obtener el auth0_user_id del token validado
    auth0_user_id = request.auth0_user.get('sub')
    
    if not auth0_user_id:
        return Response(
            {"error": "Campo 'sub' no encontrado en el token"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    data = request.data.copy()
    data['auth0_id'] = auth0_user_id

    user, created = CustomUser.objects.update_or_create(
        auth0_id=auth0_user_id,
        defaults=data
    )

    serializer = CustomUserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([])  
@permission_classes([AllowAny])
@auth0_required
def get_user_profile(request):
    auth0_user_id = request.auth0_user.get('sub')
    
    try:
        user = CustomUser.objects.get(auth0_id=auth0_user_id)
    except CustomUser.DoesNotExist:
        return Response(
            {"error": "Usuario no encontrado"}, 
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = CustomUserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([])  
@permission_classes([AllowAny])
def get_all_users(request):
    users = CustomUser.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@authentication_classes([])  
@permission_classes([AllowAny])
def delete_all_users(request):
    CustomUser.objects.all().delete()
    return Response({"message": "Todos los usuarios han sido eliminados."}, status=status.HTTP_200_OK)