from django.urls import path
from . import views

urlpatterns = [
    path('', views.customers, name='customers'),
    path('add-customers/', views.add_customers, name='add_customers'),
    path('customer-detail/<int:id>/', views.customer_detail, name='customer_detail'),
    path('edit-customer/<int:id>/', views.edit_customer, name='edit_customer'),
    path('delete-customer/<int:id>/', views.delete_customer, name='delete_customer'),
]