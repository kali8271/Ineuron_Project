from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    carat = models.FloatField()
    depth = models.FloatField()
    table = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    cut = models.CharField(max_length=20)
    color = models.CharField(max_length=2)
    clarity = models.CharField(max_length=10)
    predicted_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ${self.predicted_price} ({self.created_at:%Y-%m-%d %H:%M})"
