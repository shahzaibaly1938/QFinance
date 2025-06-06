from django.shortcuts import render, get_object_or_404
from customers.models import Customer
from sales.models import Ticketsale
from payments.models import Payment
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
import openpyxl
# Create your views here.

def customer_ledger(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    tickets = Ticketsale.objects.filter(customer=customer)
    payments = Payment.objects.filter(customer=customer)

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
    tickets = Ticketsale.objects.filter(customer=customer)
    payments = Payment.objects.filter(customer=customer)

    total_paid = sum(p.amount for p in payments)
    total_due = sum(t.amount for t in tickets) - total_paid

    template_path = 'reports/invoice_template.html'
    context = {
        'customer':customer,
        'tickets':tickets,
        'payments':payments,
        'total_paid':total_paid,
        'total_due':total_due,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename = "invoice_{customer_id}.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors with PDF generation <pre>'+ html + '</pre>')
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