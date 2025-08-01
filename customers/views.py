from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from .models import Customer
from sales.models import Ticketsale
from payments.models import Payment
from django.core.paginator import Paginator

# Create your views here.

def customers(request):
    customers = Customer.objects.all()
    s_customers = Customer.objects.all()

    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

     # Filtering logic
    customer_id = request.GET.get('customer')
    email = request.GET.get('email')
    phone = request.GET.get('phone')

    filters = {}
    if customer_id:
        filters['id'] = customer_id
    if email:
        filters['email'] = email
    if phone:
        filters['phone'] = phone


    if filters:
        customers = Customer.objects.filter( **filters).order_by('-created_at')
        paginator = Paginator(customers, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    context = {
        'customers':page_obj,
        's_customers':s_customers,
    }
    return render(request, 'customers/customers.html', context)

def add_customers(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        if Customer.objects.filter(phone=contact).exists():
            messages.error(request, "Customer phone already exists!")
            return redirect('add_customers')
        Customer.objects.create(
            name=name,
            email=email,
            phone=contact,
            address=address,
        )
        messages.success(request, "Customer created successfully!")
        return redirect('customers')
    return render(request, 'customers/add_customers.html')

def customer_detail(request, id):
    customer = Customer.objects.get(id=id)
    tickets = Ticketsale.objects.filter(customer=customer)
    payments = Payment.objects.filter(customer=customer)
    total_payments = payments.aggregate(total=Sum('amount'))['total'] or 0
    context = {
        'customer':customer,
        'tickets':tickets,
        'payments':payments,
        'total_payments':total_payments,
    }
    return render(request, 'customers/customer_detail.html', context)


def edit_customer(request, id):
    customer = Customer.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        customer.name = name
        customer.email =email
        customer.phone = phone
        customer.address = address
        customer.save()

        messages.success(request, f'{customer.name} is updated successfully')
        return redirect('customers')
    return render(request, 'customers/edit_customer.html', {'customer':customer})

def delete_customer(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    return redirect('customers')