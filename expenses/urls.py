from django.urls import path
from . import views

urlpatterns = [
    path('', views.expenses_list, name='expenses_list'),
    path('add-expenses/', views.add_expenses, name='add_expenses'),
    path('add-expenses-category/', views.add_expenses_category, name='add_expenses_category'),
    path('expense-details/<int:id>/', views.expense_detail, name='expense_detail'),
    path('edit-expenses/<int:id>/', views.edit_expenses, name='edit_expenses'),
    path('delete-expenses/<int:id>/', views.delete_expense, name='delete_expense'),
]