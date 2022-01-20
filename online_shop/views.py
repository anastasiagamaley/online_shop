from django.shortcuts import render
from store.models import Product
from django.utils.translation import activate


activate('sk')

def home(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }
    return render(request, "home.html", context)


def rules(request):
    return render(request, "rules.html")
