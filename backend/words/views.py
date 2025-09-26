from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import F
import jwt
from .models import Word, UserWord
from users.models import CustomUser
from .serializers import WordSerializer
from users.serializers import CustomUserSerializer
import random

@api_view(['GET'])
def get_word_for_user(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header or 'Bearer ' not in auth_header:
        return Response({"error": "Authorization header no encontrado o mal formateado"}, status=status.HTTP_401_UNAUTHORIZED)

    token = auth_header.split(' ')[1]

    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        auth0_user_id = decoded_token.get('sub')
    except jwt.DecodeError:
        return Response({"error": "Token inválido"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(auth0_id=auth0_user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    known_word_ids = UserWord.objects.filter(user=user).values_list('word__id', flat=True)

    unknown_words = Word.objects.exclude(id__in=known_word_ids)

    if not unknown_words.exists():
        return Response({"message": "Congrats, u know all the words"}, status=status.HTTP_200_OK)

    random_word = random.choice(unknown_words)
    serializer = WordSerializer(random_word)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_user_words_by_status(request):
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
        requesting_user = CustomUser.objects.get(auth0_id=auth0_user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    status_filter = request.GET.get('status')

    user_words_queryset = UserWord.objects.filter(user=requesting_user).select_related('word')

    if status_filter:
        if status_filter not in ['known', 'used']:
            return Response({"error": "El estado debe ser 'known' o 'used'"}, status=status.HTTP_400_BAD_REQUEST)
        user_words_queryset = user_words_queryset.filter(status=status_filter)
    else:
        user_words_queryset = user_words_queryset.filter(status__in=['known', 'used'])

    response_data = []
    for user_word_entry in user_words_queryset:
        word = user_word_entry.word
        current_status = user_word_entry.status

        word_serializer = WordSerializer(word)
        other_users_with_same_word_status = CustomUser.objects.filter(
            current_level=requesting_user.current_level,
            userword__word=word,
            userword__status=current_status
        ).exclude(id=requesting_user.id).distinct()

        other_users_serializer = CustomUserSerializer(other_users_with_same_word_status, many=True)

        item = {
            "word": word_serializer.data,
            "status": current_status,
            f"date_marked_{current_status}": user_word_entry.created_at,
            f"other_users_same_level_{current_status}_word": other_users_serializer.data
        }

        response_data.append(item)

    return Response(response_data, status=status.HTTP_200_OK)


    

@api_view(['POST'])
def mark_user_word(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header or 'Bearer ' not in auth_header:
        return Response({"error": "Authorization header no encontrado o mal formateado"}, status=status.HTTP_401_UNAUTHORIZED)

    token = auth_header.split(' ')[1]

    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        auth0_user_id = decoded_token.get('sub')
    except jwt.DecodeError:
        return Response({"error": "Token inválido"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(auth0_id=auth0_user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    word_id = request.data.get('word_id')
    new_status_value = request.data.get('status')

    if not word_id or not new_status_value:
        return Response({"error": "word_id y status son requeridos"}, status=status.HTTP_400_BAD_REQUEST)

    if new_status_value not in ['known', 'used']:
        return Response({"error": "El estado debe ser 'known' o 'used'"}, status=status.HTTP_400_BAD_REQUEST)

    word = get_object_or_404(Word, id=word_id)

    user_word_entry = UserWord.objects.filter(user=user, word=word).first()

    old_status_value = None
    if user_word_entry:
        old_status_value = user_word_entry.status

    user_word_entry, created = UserWord.objects.update_or_create(
        user=user,
        word=word,
        defaults={'status': new_status_value}
    )

    if created:
        if new_status_value == 'known':
            user.words_known_count = F('words_known_count') + 1
        elif new_status_value == 'used':
            user.words_learned_count = F('words_learned_count') + 1
    elif old_status_value != new_status_value:
        if old_status_value == 'known' and new_status_value == 'used':
            user.words_known_count = F('words_known_count') - 1
            user.words_learned_count = F('words_learned_count') + 1
        elif old_status_value == 'used' and new_status_value == 'known':
            user.words_learned_count = F('words_learned_count') - 1
            user.words_known_count = F('words_known_count') + 1

    user.save()
    user.refresh_from_db()

    if created:
        return Response({"message": f"Palabra '{word.base}' marcada como '{new_status_value}' para el usuario '{user.username}'. Contadores actualizados.", "user_counts": {"known": user.words_known_count, "learned": user.words_learned_count}}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": f"Estado de la palabra '{word.base}' actualizado a '{new_status_value}' para el usuario '{user.username}'. Contadores actualizados.", "user_counts": {"known": user.words_known_count, "learned": user.words_learned_count}}, status=status.HTTP_200_OK)