from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.user.username