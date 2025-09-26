from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CustomUser
        fields = [
            'id',
            'auth0_id',
            'username',
            'profile_picture_url',
            'current_level',
            'words_known_count',
            'words_learned_count',
            'sentences_correct_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']