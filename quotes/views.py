from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
# Create your views here.

quotes = ["I like criticism. It makes you strong.", "The biggest dreams aren't fueled by belief, they're fueled by doubt.", "If you quit once it becomes a habit. Never quit!"]
images = ["https://media.printler.com/media/photo/141736.jpg", "https://media.printler.com/media/photo/141746.jpg", "https://media.printler.com/media/photo/125058.jpg"]

def quote_page(request):
    index = random.randrange(len(quotes))
    context = {
        "quote": quotes[index],
        "image": images[index]
    }
    return render(request, "quotes/quote.html", context)

def show_all_page(request):
    context = {
        "quotes": quotes,
        "images": images
    }
    return render(request, "quotes/show_all.html", context)

def about_page(request):
    return render(request, "quotes/about.html")