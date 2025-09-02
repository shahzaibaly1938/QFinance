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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer')
    pnr = models.CharField(max_length=100)
    airline = models.ForeignKey(Airline ,on_delete=models.CASCADE, related_name='airline')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    manual_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT, null=True, blank=True)
    reserve_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    flight_type = models.CharField(max_length=30, default='')
    no_of_adults = models.PositiveIntegerField(default=0)
    no_of_children = models.PositiveIntegerField(default=0)
    no_of_infants = models.PositiveIntegerField(default=0)
    reference = models.CharField(max_length=100)
    paid = models.CharField(max_length=30, choices=[("paid", "Paid"), ("unpaid", "Unpaid")], default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.pnr}"
    

class Route(models.Model):
    ticket = models.ForeignKey(Ticketsale, on_delete=models.CASCADE, related_name='routes')
    from_destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='route_from')
    to_destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='route_to')
    departure_date = models.DateField()

    def __str__(self):
        return f"{self.from_destination.name} to {self.to_destination.name} on {self.departure_date}"


class Adults(models.Model):
    ticket = models.ForeignKey(Ticketsale, on_delete=models.CASCADE, related_name='adults')
    name = models.CharField(max_length=255, default=None, null=True, blank=True)
    dob = models.DateField(default=None, null=True, blank=True)
    nationality = models.CharField(max_length=100, default=None, null=True, blank=True)
    id_number = models.CharField(max_length=100, default=None, null=True, blank=True)
    passport_number = models.CharField(max_length=100, default=None, null=True, blank=True)

    def __str__(self):
        return self.name

class Childs(models.Model):
    ticket = models.ForeignKey(Ticketsale, on_delete=models.CASCADE, related_name='childs')
    name = models.CharField(max_length=255, default=None, null=True, blank=True)
    dob = models.DateField(default=None, null=True, blank=True)
    nationality = models.CharField(max_length=100, default=None, null=True, blank=True)
    id_number = models.CharField(max_length=100, default=None, null=True, blank=True)
    passport_number = models.CharField(max_length=100, default=None, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Infants(models.Model):
    ticket = models.ForeignKey(Ticketsale, on_delete=models.CASCADE, related_name='infants')
    name = models.CharField(max_length=255, default=None, null=True, blank=True)
    dob = models.DateField(default=None, null=True, blank=True)

    def __str__(self):
        return self.name
    