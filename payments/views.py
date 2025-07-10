from django.shortcuts import render,redirect
from .models import Payment
from customers.models import Customer
from sales.models import Ticketsale
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.

def payments(request):
    payments = Payment.objects.all().order_by('-date')
    paginator = Paginator(payments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    customers = Customer.objects.all()
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
        payment = Payment(customer=customer, amount=ticket.amount, method=payment_method, date=date, notes=notes)
        payment.save()
        ticket.paid = 'paid'
        ticket.save()
        messages.success(request, f"Amount: {ticket.amount} paid by {customer.name} successfully!")
        return redirect('unpaid_tickets')
    return render(request, 'payments/add_payments.html', {'ticket': ticket, 'customer': customer})

def unpaid_tickets(request):
    customer = Customer.objects.all()
    tickets_unpaid = Ticketsale.objects.filter(paid='unpaid')

    context = {
        'customers':customer,
        'unpaid_tickets':tickets_unpaid,
    }
    return render(request, 'payments/unpaid_tickets.html', context)

def edit_payment(request, id):
    customers = Customer.objects.all()
    context = {
        'customers':customers,
    }
    return render(request,'payments/edit_payment.html', context)


def delete_payment(request, id):
    payment = Payment.objects.get(id=id)
    payment.delete()
    messages.success(request, f'Your {payment.amount} amount is deleted successfully!')
    return redirect('payments')