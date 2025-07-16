from django.shortcuts import render, get_object_or_404
from customers.models import Customer
from sales.models import Ticketsale
from payments.models import Payment
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.db.models import Sum
from django.core.paginator import Paginator
from django.template.loader import get_template
import openpyxl
from datetime import date
# Create your views here.

def reports(request):
    customers = Customer.objects.all()
    payments = Payment.objects.all()
    paginator = Paginator(payments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total_payments = payments.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    total_invoice_generated = Ticketsale.objects.count()
    total_customer = customers.count()


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
        'customers': customers,
        'payments': page_obj,
        'total_payments': total_payments,
        'total_invoice_generated': total_invoice_generated,
        'total_customer': total_customer,
    }
    return render(request, 'reports/reports.html', context)


def customer_ledger(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    tickets = Ticketsale.objects.filter(customer=customer)
    payments = Payment.objects.filter(customer=customer)


     # Filtering logic
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    filters = {}
    if start_date:
        filters['reserve_date__gte'] = start_date
    if end_date:
        filters['reserve_date__lte'] = end_date


    if filters:
        tickets = Ticketsale.objects.filter(customer=customer, **filters).order_by('-reserve_date')
        payments = Payment.objects.filter(ticket__in=tickets).order_by('-date')
        # paginator = Paginator(payment, 20)
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)

    total_paid = sum(p.amount for p in payments)
    total_due = sum(t.amount for t in tickets) - total_paid

    return render(request, 'reports/customer_ledger.html', {
        'customer':customer,
        'tickets':tickets,
        'payments':payments,
        'total_paid':total_paid,
        'total_due':total_due,
    })



def generate_invoice(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    # Get date filters from request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    filters = {}
    if start_date:
        filters['reserve_date__gte'] = start_date
    if end_date:
        filters['reserve_date__lte'] = end_date

    tickets = Ticketsale.objects.filter(customer=customer, **filters)
    payments = Payment.objects.filter(customer=customer)

    # Optionally, filter payments by tickets in the date range
    if filters:
        payments = payments.filter(ticket__in=tickets)

    total_paid = sum(p.amount for p in payments)
    total_due = sum(t.amount for t in tickets) - total_paid

    template_path = 'reports/invoice_template.html'
    context = {
        'customer': customer,
        'tickets': tickets,
        'payments': payments,
        'total_paid': total_paid,
        'total_due': total_due,
        'start_date': start_date,
        'end_date': end_date,
        'today':date.today(),
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="invoice_{customer_id}.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors with PDF generation <pre>' + html + '</pre>')
    return response


def export_ticket_sales(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Ticket Sales"

    #add headers
    header = ['Date', 'Agent', 'Customer', 'Price', 'Status']
    ws.append(header)

    #add data
    sales = Ticketsale.objects.select_related('agent', 'customer').all()
    for sale in sales:
        ws.append([
            sale.reserve_date.strftime('%Y-%m-%d'),
            sale.agent.user.username,
            sale.customer.name,
            float(sale.amount),
            'Paid' if sale.paid else 'Due',
        ])

    #Create Response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=ticket_sales.xlsx'
    wb.save(response)
    return response