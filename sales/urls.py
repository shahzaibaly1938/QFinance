from django.urls import path
from . import views

urlpatterns = [
    path('ticket-sales/', views.ticket_sale, name='ticket_sale'),
    path('new-ticket/', views.add_ticket, name='add_ticket'),
    path('ticket-detail/<int:id>/', views.ticket_detail, name='ticket_detail'),                
    path('edit-ticket/<int:id>/', views.edit_ticket, name='edit_ticket'),                
    path('delete-ticket/<int:id>/', views.delete_ticket, name='delete_ticket'),
]