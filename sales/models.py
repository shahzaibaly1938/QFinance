from django.db import models
from customers.models import Customer
from users.models import Agent

# Create your models here.
class Airline(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Destination(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Ticketsale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pnr = models.CharField(max_length=100)
    airline = models.ForeignKey(Airline ,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reserve_date = models.DateField()
    flight_date = models.DateField()
    flight_from = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='flight_from', default='')
    flight_to = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='flight_to', default='')
    notes = models.TextField(blank=True, null=True)
    reference = models.CharField(max_length=100)
    paid = models.CharField(max_length=30, choices=[("paid", "Paid"), ("unpaid", "Unpaid")], default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.pnr}"

    