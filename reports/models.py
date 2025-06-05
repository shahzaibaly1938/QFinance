from django.db import models
from customers.models import Customer
# Create your models here.

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    issue_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=[("paid", "Paid"), ("unpaid", "Unpaid")])

    def __str__(self):
        return f"Invoice #{self.id} - {self.customer.name}"