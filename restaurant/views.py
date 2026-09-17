from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random, time
# Create your views here.

specials = ["Pralines & Cream", "Earl Grey Tea", "Hojicha", "Strawberry Shortcake", "Matcha", "Brown Sugar Boba", "Mango Sorbet"]

def main_page(request):
    return render(request, "restaurant/main.html")

def order_page(request):
    context = {
        "special": random.choice(specials)
    }
    return render(request, "restaurant/order.html", context)

def show_confirmation_page(request):
    return render(request, "confirmation.html")

def submit_confirmation_page(request):
    print(request)