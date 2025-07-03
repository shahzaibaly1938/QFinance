from django.urls import path
from . import views

urlpatterns = [
        path('add-payment/', views.add_payment, name='add_payment'),
]