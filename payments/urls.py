from django.urls import path
from . import views

urlpatterns = [
        path('', views.payments, name='payments'),
        path('details/<int:id>/', views.payment_detail, name='payment_detail'),
        path('add-payment/', views.add_payment, name='add_payment'),
        path('edit-payment/<int:id>/', views.edit_payment, name='edit_payment'),
]