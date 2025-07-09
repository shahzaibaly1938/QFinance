from django.shortcuts import render, redirect
from .models import Expense, Expense_category
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
def expenses_list(request):
    expense_category = Expense_category.objects.all()
    expenses = Expense.objects.all().order_by('-date')
    paginator = Paginator(expenses, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories':expense_category,
        'expenses': page_obj,
    }
    return render(request, 'expenses/expenses_list.html', context)


def expense_detail(request, id):
    expense = Expense.objects.get(id=id)
    return render(request, 'expenses/expense_details.html', {'expense':expense})

def add_expenses(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        desc = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        expense = Expense(
            category=Expense_category.objects.get(id=category),
            description=desc, amount=amount, date=date,
            )
        expense.save()
        messages.success(request, 'Expense added successfully.')
        return redirect('expenses_list')
    expense_category = Expense_category.objects.all()
    return render(request, 'expenses/add_expenses.html',{'categories':expense_category})

def add_expenses_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        expense_category = Expense_category(name=name)
        expense_category.save()
        messages.success(request, 'Expense Category added successfully.')
        return redirect('add_expenses_category')
    return render(request, 'expenses/add_expenses_category.html')


def edit_expenses(request, id):
    if request.method == 'POST':
        category = request.POST.get('category')
        desc = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')

        u_expense = Expense.objects.get(id=id)
        u_expense.category = Expense_category.objects.get(id=category)
        u_expense.description = desc
        u_expense.amount = amount
        u_expense.date = date
        u_expense.save()
        messages.success(request, 'Expense updates successfully!')
        return redirect('expenses_list')
    

    expense = Expense.objects.get(id=id)
    expense_category = Expense_category.objects.all()

    context = {
        'expense':expense,
        'categories':expense_category,
    }
    return render(request, 'expenses/edit_expenses.html', context)

def delete_expense(request, id):
    expense = Expense.objects.get(id=id)
    expense.delete()
    messages.success(request, f'Your {expense.category} expense is deleted successfully!')
    return redirect('expenses_list')