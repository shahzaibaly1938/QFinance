from django.shortcuts import render, redirect
from .models import Ticketsale, Destination, Airline
from customers.models import Customer
from users.models import Agent
from django.contrib import messages
from django.core.paginator import Paginator
from decimal import Decimal

# Create your views here.
def ticket_sale(request):
    tickets = Ticketsale.objects.all().order_by('-reserve_date')
    paginator = Paginator(tickets, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    customers = Customer.objects.all()
    agents = Agent.objects.all()
    destinations = Destination.objects.all()

    context = {
        'tickets':page_obj,
        'customers':customers,
        'agents':agents,
        'destinations':destinations,
    }
    return render(request, 'sales/ticket_sale.html', context)


def add_ticket(request):
    if request.method == 'POST':
        customer = request.POST.get('customer')
        commission_agent = request.POST.get('agent')
        pnr = request.POST.get('pnr')
        airline = request.POST.get('airline')
        amount = request.POST.get('amount')
        reserve_date = request.POST.get('reserve_date')
        flight_date = request.POST.get('flight_date')
        flight_from = request.POST.get('flight_from')
        flight_to = request.POST.get('flight_to')
        reference = request.POST.get('reference')
        payment = request.POST.get('payment')
        notes = request.POST.get('notes')

        agent = Agent.objects.get(id=commission_agent)

        amount_decimal = Decimal(amount)
        ticket = Ticketsale(
            customer=Customer.objects.get(id=customer),
            commission=amount_decimal * agent.commission_rate,
            pnr=pnr,
            airline=Airline.objects.get(id=airline),
            amount=amount_decimal,
            reserve_date=reserve_date,
            flight_date=flight_date,
            flight_from=Destination.objects.get(id=flight_from),
            flight_to=Destination.objects.get(id=flight_to),
            reference=reference,
            paid=payment,
            notes=notes,
        )
        ticket.save()
        return redirect('payment_process', ticket.id)
        

    customers = Customer.objects.all()
    commission_agent = Agent.objects.all()
    destinations = Destination.objects.all()
    airlines = Airline.objects.all()

    context = {
        'customers':customers,
        'commission_agent':commission_agent,
        'destinations':destinations,
        'airlines':airlines,
    }
    return render(request, 'sales/add_ticket.html', context)

def payment_process(request, id):
    ticket = Ticketsale.objects.get(id=id)
    return render(request, 'sales/payment_step.html', {'ticket':ticket})

def ticket_detail(request, id):
    ticket = Ticketsale.objects.get(id=id)
    return render(request, 'sales/ticket_detail.html', {'ticket':ticket})

def delete_ticket(request, id):
    ticket = Ticketsale.objects.get(id=id)
    ticket.delete()
    messages.success(request, f'Ticket: {ticket.pnr} of {ticket.customer.name} is deleted successfully!')
    return redirect('ticket_sale')

def edit_ticket(request, id):
    if request.method == 'POST':
        customer = request.POST.get('customer')
        agent = request.POST.get('agent')
        pnr = request.POST.get('pnr')
        airline = request.POST.get('airline')
        amount = request.POST.get('amount')
        reserve_date = request.POST.get('reserve_date')
        flight_date = request.POST.get('flight_date')
        flight_from = request.POST.get('flight_from')
        flight_to = request.POST.get('flight_to')
        reference = request.POST.get('reference')
        payment = request.POST.get('payment')
        notes = request.POST.get('notes')

        ticket = Ticketsale.objects.get(id=id)
    
        ticket.customer=Customer.objects.get(id=customer)
        ticket.agent = Agent.objects.get(id=agent)
        ticket.pnr = pnr
        ticket.airline = Airline.objects.get(id=airline)
        ticket.amount = amount
        ticket.reserve_date = reserve_date
        ticket.flight_date = flight_date
        ticket.flight_from = Destination.objects.get(id=flight_from)
        ticket.flight_to = Destination.objects.get(id=flight_to)
        ticket.reference = reference
        ticket.paid = payment
        ticket.notes = notes

        ticket.save()

        return redirect('ticket_sale')

    ticket = Ticketsale.objects.get(id=id)
    customers = Customer.objects.all()
    agents = Agent.objects.all()
    destinations = Destination.objects.all()
    airlines = Airline.objects.all()

    context = {
        'customers':customers,
        'agents':agents,
        'destinations':destinations,
        'airlines':airlines,
        'ticket':ticket,
    }
    return render(request, 'sales/edit_ticket.html', context)


def add_airline(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        airline = Airline(name=name)
        airline.save()
        messages.success(request, 'Airline added successfully!')
        return redirect('add_airline')
    return render(request, 'sales/add_airlines.html')

def add_destination(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        destination = Destination(name=name)
        destination.save()
        messages.success(request, 'Destination added successfully!')
        return redirect('add_destination')
    return render(request, 'sales/add_destinations.html')