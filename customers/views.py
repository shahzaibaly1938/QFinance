from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer

# Create your views here.

def add_customers(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        Customer.objects.create(
            name=name,
            email=email,
            phone=contact,
            address=address,
        )
        messages.success(request, "Customer created successfully!")
        return redirect('add_customers')
    return render(request, 'customers/add_customers.html')