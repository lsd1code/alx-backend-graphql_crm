from django.shortcuts import render
from django.http import HttpResponse

from .models import Product, Customer, Order

from datetime import date

def index(request):
    c = Customer.objects.all()

    date.today

    with open('path', 'w') as f:
        f.write('')

    return HttpResponse()