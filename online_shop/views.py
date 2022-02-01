from django.shortcuts import render, redirect
from store.models import Product
from orders.models import OrderProduct
from django.utils.translation import activate
from store.forms import ReviewForm
from store.models import ReviewRating
from django.contrib import messages
from django.contrib.auth import authenticate


activate('sk')

def home(request):
    products = Product.objects.all().filter(is_available=True)

    # check if customer odred anithing to white review
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, ordered=True).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    reviews = ReviewRating.objects.filter(status=True)

    context = {
    'products': products,
    'orderproduct': orderproduct,
    'reviews': reviews,
        }
    return render(request, "home.html", context)




def rules(request):
    return render(request, "rules.html")


def submit_review(request):
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Ďakujem za Vaše hodnotenie!')
            return redirect('home')
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Ďakujem za Vaše hodnotenie!')
                return redirect('home')
