# Views for the various pages, adding context for HTML
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random, time
# Create your views here.

# Daily special list
specials = ["Pralines & Cream", "Earl Grey Tea", "Hojicha", "Strawberry Shortcake", "Matcha", "Brown Sugar Boba", "Mango Sorbet"]

def main_page(request):
    ''' Goes to the main page '''
    return render(request, "restaurant/main.html")

def order_page(request):
    ''' Goes to the order page with context for a random special '''
    context = {
        "special": random.choice(specials) # Random daily item
    }
    return render(request, "restaurant/order.html", context)

def confirmation_page(request):
    ''' Processes submission and shows receipt '''
    if request.method == "POST":
        items = []
        total = 0
        customer_name = request.POST.get("customer_name", "")
        customer_email = request.POST.get("customer_email", "")
        special_instructions = request.POST.get("special_instructions", "")

        # Prices for each key
        prices = {
            "vanilla": 4.00,
            "chocolate": 4.50,
            "strawberry": 4.25,
            "milkshake": 5.00,
            "daily_special": 6.00,
        }

        # HTML label assignment
        labels = {
            "vanilla": "Vanilla Cone",
            "chocolate": "Chocolate Cone",
            "strawberry": "Strawberry Cone",
            "milkshake": "Milkshake",
            "daily_special": "Daily Special",
        }

        # Calculate total price
        for key in prices:
            if request.POST.get(key):
                items.append(labels[key])
                total += prices[key]

        ready_seconds = random.randint(30 * 60, 60 * 60)
        readytime = time.strftime(
            "%I:%M %p",
            time.localtime(time.time() + ready_seconds)
        )

        context = {
            "items": items,
            "total": total,
            "readytime": readytime,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "special_instructions": special_instructions,
        }
        return render(request, "restaurant/confirmation.html", context)

    return render(request, "restaurant/confirmation.html", {
        "items": [],
        "total": 0,
        "readytime": "",
        "customer_name": "",
        "customer_email": "",
        "special_instructions": "",
    })

