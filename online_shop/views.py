from django.shortcuts import render, redirect
from store.models import Product
from orders.models import OrderProduct
from django.utils.translation import activate
from store.forms import ReviewForm
from store.models import ReviewRating
from accounts.models import UserApi
from django.contrib import messages
from django.contrib.auth import authenticate
from django.db.models import Avg
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .forms import ContactForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import BadHeaderError, EmailMessage
from django.template.loader import render_to_string
from django.db.models import Q

activate('sk')

def home(request):
    products = Product.objects.all().filter(is_available=True)

    reviews = None

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
    averagereviews = ReviewRating.objects.filter(status=True, parent_id=None).aggregate(average=Avg('rating'))
    if averagereviews['average'] is not None:
        avg = float(averagereviews['average'])
    # visits on page
    def get_ip(request):
        address = request.META.get('HTTP_X_FORWARDED_FOR')
        if address:
            ip = address.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    ip = get_ip(request)
    u = UserApi(user=ip)
    result = UserApi.objects.filter(Q(user__icontains=ip))
    if len(result)==1:
        pass
    elif len(result)>1:
        pass
    else:
        u.save()
    num_visits = UserApi.objects.all().count()



    context = {
    'products': products,
    'orderproduct': orderproduct,
    'reviews': reviews,
    'avg': avg,
    'num_visits': num_visits,
        }
    return render(request, "home.html", context)


    averagereviews = ReviewRating.objects.filter(status=True, parent=None).agrigate(average=Avg('rating'))
    avg = 0
    if averagereviews['average'] is not None:
        avg = float(reviews['average'])
    return avg

# def visits(request):
#     num_visits = request.session.get('num_visits', 0)
#     request.session['num_visits'] = num_visits + 1
#     return num_visits



def rules(request):
    return render(request, "rules.html")


def submit_review(request):
    if request.method == "POST":
        # try:
        #     reviews = ReviewRating.objects.get(user__id=request.user.id)
        #     form = ReviewForm(request.POST, instance=reviews)
        #     form.save()
        #     messages.success(request, 'Ďakujem za Vaše!')
        #     return redirect('home')
        # except ReviewRating.DoesNotExist:
        form = ReviewForm(request.POST)
        if form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_qs = ReviewRating.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    parent_obj = parent_qs.first()
            data = ReviewRating()
            try:
                data.subject = form.cleaned_data['subject']
            except:
                data.subject = None
            try:
                data.rating = form.cleaned_data['rating']
            except:
                data.rating = None
            data.review = form.cleaned_data['review']
            data.ip = request.META.get('REMOTE_ADDR')
            data.user_id = request.user.id
            data.parent = parent_obj
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

def policy(request):
    return render(request, 'policy.html')
