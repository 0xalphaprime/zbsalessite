from django.shortcuts import render, redirect
from .models import Customer, Invoice
import datetime
from collections import defaultdict

# Create your views here.
def index(request):
    return render(request, 'sales/index.html')

def customer_list(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers
    }
    return render(request, 'sales/customer_list.html', context)

def customer_detail(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    today = datetime.datetime.now().date()
    start_of_year = datetime.date(today.year, 1, 1)
    invoices = Invoice.objects.filter(customer=customer, billed_on__gte=start_of_year)
    month_totals = defaultdict(int)
    for invoice in invoices:
        month_totals[invoice.billed_on.month] += invoice.total()
    context = {
        'customer': customer,
        'invoices': invoices,
        'month_totals': month_totals
    }
    return render(request, 'sales/customer_detail.html', context)



