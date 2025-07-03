from django.shortcuts import render

# Create your views here.
def add_payment(request):
    return render(request, 'payments/add_payments.html')