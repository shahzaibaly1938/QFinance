from django.shortcuts import render,redirect
from .models import Payment
from customers.models import Customer
from sales.models import Ticketsale
from django.contrib import messages
from django.core.paginator import Paginator
from users.models import Agent

# Create your views here.

def payments(request):
    payments = Payment.objects.all().order_by('-date')
    paginator = Paginator(payments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    customers = Customer.objects.all()

    # Filtering logic
    customer_id = request.GET.get('customer')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    filters = {}
    if customer_id:
        filters['customer_id'] = customer_id
    if start_date:
        filters['date__gte'] = start_date
    if end_date:
        filters['date__lte'] = end_date


    if filters:
        payment = Payment.objects.filter( **filters).order_by('-date')
        paginator = Paginator(payment, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)



    context = {
        'payments': page_obj,
        'customers':customers,
    }
    return render(request, 'payments/payments.html', context)

def payment_detail(request, id):
    payment = Payment.objects.get(id=id)
    context = {
        'payment':payment
    }
    return render(request, 'payments/payment_detail.html', context)

def add_payment(request, id):
    ticket = Ticketsale.objects.get(id=id)
    customer = ticket.customer
    if request.method == 'POST':
        payment_method = request.POST.get('method')
        date = request.POST.get('date')
        notes = request.POST.get('notes')
        payment = Payment(customer=customer, ticket=ticket, amount=ticket.amount, method=payment_method, date=date, notes=notes)
        payment.save()
        ticket.paid = 'paid'
        ticket.save()
        messages.success(request, f"Amount: {ticket.amount} paid by {customer.name} successfully!")
        return redirect('unpaid_tickets')
    return render(request, 'payments/add_payments.html', {'ticket': ticket, 'customer': customer})

def unpaid_tickets(request):
    customer = Customer.objects.all()
    agents = Agent.objects.all()
    tickets_unpaid = Ticketsale.objects.filter(paid='unpaid').order_by('-reserve_date')
    paginator = Paginator(tickets_unpaid, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

     # Filtering logic
    agent_id = request.GET.get('agent')
    customer_id = request.GET.get('customer')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    filters = {}
    if agent_id:
        filters['agent_id'] = agent_id
    if customer_id:
        filters['customer_id'] = customer_id
    if start_date:
        filters['reserve_date__gte'] = start_date
    if end_date:
        filters['reserve_date__lte'] = end_date


    if filters:
        tickets = Ticketsale.objects.filter(paid='unpaid', **filters).order_by('-reserve_date')
        paginator = Paginator(tickets, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    context = {
        'customers':customer,
        'unpaid_tickets':page_obj,
        'agents':agents,
    }
    return render(request, 'payments/unpaid_tickets.html', context)

def edit_payment(request, id):
    payment = Payment.objects.get(id=id)
    customer = payment.customer
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('method')
        date = request.POST.get('date')
        notes = request.POST.get('notes')

        payment.amount = amount
        payment.method = payment_method
        payment.date = date
        payment.notes = notes
        payment.save()
        messages.success(request, f"{customer} payment is updated successfully!")
        return redirect('payments')

    context = {
        'customer':customer,
        'payment':payment,
    }
    return render(request,'payments/edit_payment.html', context)


def delete_payment(request, id):
    payment = Payment.objects.get(id=id)
    if payment.ticket:
        messages.info(request, 'Cannot delete payment because it is linked to a ticket.')
        return redirect('payments')
    payment.delete()
    messages.success(request, f'Your {payment.amount} amount is deleted successfully!')
    return redirect('payments')