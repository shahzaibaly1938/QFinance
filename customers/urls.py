from django.urls import path
from . import views

urlpatterns = [
    path('add-customers/', views.add_customers, name='add_customers'),
]