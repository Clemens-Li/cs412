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

        # Main item prices
        prices = {
            "vanilla": 4.00,
            "chocolate": 4.50,
            "strawberry": 4.25,
            "milkshake": 5.00,
            "daily_special": 6.00,
        }

        labels = {
            "vanilla": "Vanilla Cone",
            "chocolate": "Chocolate Cone",
            "strawberry": "Strawberry Cone",
            "milkshake": "Milkshake",
            "daily_special": "Daily Special",
        }

        toppings = { #extra toppings
            "chocolate_chips": ("Chocolate Chips", 1.00),
            "whipped_cream": ("Whipped Cream", 1.25),
            "sprinkles": ("Sprinkles", 0.75),
            "caramel": ("Caramel Drizzle", 1.50),
        }

        # Calculate total price
        for key in prices:
            if request.POST.get(key):
                items.append(labels[key])
                total += prices[key]

        for key, (label, price) in toppings.items():
            if request.POST.get(key):
                items.append(f"{label} (+${price:.2f})")
                total += price

        ready_seconds = random.randint(30 * 60, 60 * 60) # Ready time randomizer
        readytime = time.strftime(
            "%I:%M %p",
            time.localtime(time.time() + ready_seconds)
        )

        context = { # context dictionary
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

