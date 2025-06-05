from django.db import models
from customers.models import Customer

# Create your models here.
class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, choices=[("cash", "Cash"),("bank","Bank Transfer"), ("card","Card")])
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer.name} - Rs.{self.amount}"