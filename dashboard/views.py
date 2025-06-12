from django.shortcuts import render
from django.db.models import Sum
from django.utils.timezone import now
from sales.models import Ticketsale
from expenses.models import Expense
from users.models import Agent
from customers.models import Customer
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard(request):
    current_month = now().month
    current_year = now().year

    #Get filter from request
    agent_id = request.GET.get('agent')
    customer_id = request.GET.get('customer')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    sales = Ticketsale.objects.all()

    if agent_id:
        sales = sales.filter(agent_id=agent_id)

    if customer_id:
        sales = sales.filter(customer_id=customer_id)

    if start_date and end_date: 
        sales = sales.filter(reserve_date__range=[start_date, end_date])

    else:
        sales = sales.filter(reserve_date__year=current_year, reserve_date__month = current_month)

    total_sales_amount = sales.aggregate(total=Sum('amount'))['total'] or 0
    total_tickets = sales.count()

    monthly_expense = Expense.objects.filter(date__year=current_year, date__month=current_month)

    total_expense = monthly_expense.aggregate(total=Sum('amount'))['total'] or 0
  
    agent = Agent.objects.get(user=request.user)
    commission_rate = agent.commission_rate
    total_commission = total_sales_amount * commission_rate
    total_profit = total_commission - total_expense


    # Add this to your dashboard view
    monthly_sales_data = (
        Ticketsale.objects
        .annotate(month=TruncMonth('reserve_date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    months = []
    sales = []

    for entry in monthly_sales_data:
        month_name = entry['month'].strftime('%B')
        months.append(month_name)
        sales.append(float(entry['total']))



    context = {
        'agents': Agent.objects.all(),
        'customers': Customer.objects.all(),
        'total_sales':total_sales_amount,
        'total_tickets':total_tickets,
        'total_expense':total_expense,
        'total_commission':total_commission,
        'total_profit':total_profit,
        'months': months,
        'sales': sales,
    }

    return render(request, 'dashboard/dashboard.html', context)