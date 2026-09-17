from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random, time
# Create your views here.

def main_page(request):
    return render(request, "restaurant/main.html")

def order_page(request):
    return

def confirmation_page(request):
    return