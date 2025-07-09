from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Agent(models.Model):
    commission_agent = models.CharField(max_length=200, default='')
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.commission_agent} Rate : {self.commission_rate}"