from django.shortcuts import render, redirect
from store.models import Product
from orders.models import OrderProduct
from django.utils.translation import activate
from store.forms import ReviewForm
from store.models import ReviewRating
from django.contrib import messages
from django.contrib.auth import authenticate
from django.db.models import Avg

from .forms import ContactForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import BadHeaderError, EmailMessage
from django.template.loader import render_to_string


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
    # average rating calculation
    averagereviews = ReviewRating.objects.filter(status=True).aggregate(average=Avg('rating'))
    avg = 0
    if averagereviews['average'] is not None:
        avg = float(averagereviews['average'])

    context = {
    'products': products,
    'orderproduct': orderproduct,
    'reviews': reviews,
    'avg': avg,
        }
    return render(request, "home.html", context)


    averagereviews = ReviewRating.objects.filter(status=True).agrigate(average=Avg('rating'))
    avg = 0
    if averagereviews['average'] is not None:
        avg = float(reviews['average'])
    return avg

def visits(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return num_visits



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


def company(request):
    return render(request, "company.html")


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            mail_subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            messagetext = form.cleaned_data['message']
            message = render_to_string('accounts/contact_email.html', {
                'from_email': from_email,
                'messagetext': messagetext,
            })
            to_email = 'anastasiagamaley@gmail.com'
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            try:
                send_email.send()
            except BadHeaderError:
                return HttpResponse('Vyplnite vsetky polia')
            messages.success(request, 'Vas email bol odoslaný')
            return render(request, "contact.html", {'form': form})
    else:
        return render(request, "contact.html", {'form': form})



def dtf(request):
    return render(request, "dtf.html")
