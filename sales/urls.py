from django.urls import path
from . import views

urlpatterns = [
    path('ticket-sales/', views.ticket_sale, name='ticket_sale'),
    path('new-ticket/', views.add_ticket, name='add_ticket'),
    path('ticket-detail/<int:id>/', views.ticket_detail, name='ticket_detail'),                
    path('payment-processing/<int:id>/', views.payment_process, name='payment_process'),                
    path('edit-ticket/<int:id>/', views.edit_ticket, name='edit_ticket'),                
    path('delete-ticket/<int:id>/', views.delete_ticket, name='delete_ticket'),
    path('add-airlines/', views.add_airline, name='add_airline'),
    path('add-destination/', views.add_destination, name='add_destination'),
]