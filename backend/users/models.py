from django.db import models

# Create your models here.

class CustomUser(models.Model):
    auth0_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=100)
    profile_picture_url = models.URLField(blank=False, null=False)
    current_level = models.CharField(max_length=20)
    words_known_count = models.IntegerField(default=0)
    words_learned_count = models.IntegerField(default=0)
    sentences_correct_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def __str__(self):
        return self.username