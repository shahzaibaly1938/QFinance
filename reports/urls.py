from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports, name='reports'),
    path('<int:customer_id>/customer_ledger/', views.customer_ledger, name='customer_ledger'),
    path('<int:customer_id>/invoice/', views.generate_invoice, name='generate_invoice'),
    path('export-ticket-sales/', views.export_ticket_sales, name='export_ticket_sales'),
]