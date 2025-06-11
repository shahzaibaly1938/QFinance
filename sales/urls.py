from django.urls import path
from . import views

urlpatterns = [
    path('ticket-sales/', views.ticket_sale, name='ticket_sale'),
    path('new-ticket/', views.add_ticket, name='add_ticket'),
]