from django.shortcuts import render
from .models import Ticketsale, Destination, Airline
from customers.models import Customer
from users.models import Agent

# Create your views here.
def ticket_sale(request):
    tickets = Ticketsale.objects.all()
    customers = Customer.objects.all()
    agents = Agent.objects.all()
    destinations = Destination.objects.all()

    context = {
        'tickets':tickets,
        'customers':customers,
        'agents':agents,
        'destinations':destinations,
    }
    return render(request, 'sales/ticket_sale.html', context)


def add_ticket(request):
    if request.method == 'POST':
        pass
    customers = Customer.objects.all()
    agents = Agent.objects.all()
    destinations = Destination.objects.all()
    airlines = Airline.objects.all()

    context = {
        'customers':customers,
        'agents':agents,
        'destinations':destinations,
        'airlines':airlines,
    }
    return render(request, 'sales/add_ticket.html', context)