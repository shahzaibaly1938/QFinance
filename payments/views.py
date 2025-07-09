from django.shortcuts import render
from .models import Payment
from customers.models import Customer
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

def add_payment(request):
    return render(request, 'payments/add_payments.html')

def edit_payment(request, id):
    customers = Customer.objects.all()
    context = {
        'customers':customers,
    }
    return render(request,'payments/edit_payment.html', context)