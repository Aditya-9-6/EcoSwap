from django.db import models
from django.contrib.auth.models import User

class UserScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    plastic_saved = models.IntegerField(default=0) # Estimated grams saved

    def __str__(self):
        return f"{self.user.username} - {self.points}"

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query
