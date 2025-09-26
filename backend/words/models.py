from django.db import models
from users.models import CustomUser

# Create your models here.

class Word(models.Model):
    base = models.CharField(max_length=100)
    s_form = models.CharField(max_length=100)
    past = models.CharField(max_length=100) 
    past_participle = models.CharField(max_length=100)
    ing = models.CharField(max_length=100)
    meaning = models.CharField(max_length=100)
    example = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)

    def __str__(self):
        return self.base


class UserWord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'word')

    def __str__(self):
        return f"{self.user.username} → {self.word.base}"