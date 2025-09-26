from django.db import models
# Create your models here.

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user.username} → {self.achievement.name}"
