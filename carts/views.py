from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import QuantityForm


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    #if user is is_authenticated
    if current_user.is_authenticated:

        try:
            cart_item = CartItem.objects.get(product=product, user=current_user)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            cart_item.save()
        return redirect('cart')
    #if user is not is_authenticated
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) #get the cart ussing cart id present in session_key
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()



        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            cart_item.save()
        return redirect('cart')
# Create your views here.

# def add_cart_amount(request, product_id, amount):
#
#     product = get_object_or_404(Product, id=product_id)
#
#     if request.user.is_authenticated:
#         cart_item = CartItem.objects.get(product=product, user=request.user)
#     else:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#         cart_item = CartItem.objects.get(product=product, cart=cart,)
#     if amount != 0:
#         cart_item.quantity = amount
#         cart_item.save()
#     else:
#         pass
#
#     return redirect('cart')


#
def remove_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart,)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def add_cart_amount(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user)
            form = QuantityForm(request.POST, instance=request.user)
            if form.is_valid():
                cart_item.quantity = form.cleaned_data['quantity']
                cart_item.save()
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart)
            form = QuantityForm(request.POST, instance=cart)
            if form.is_valid():
                cart_item.quantity = form.cleaned_data['quantity']
                cart_item.save()

    return redirect('cart')



def remove_cart_item(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')



def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        # form = QuantityForm(request.POST)
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += float("{:.2f}".format(cart_item.product.price * cart_item.quantity))
            quantity += cart_item.quantity
        tax = float("{:.2f}".format((20 * total)/100))
        grand_total = float("{:.2f}".format(total + tax))
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        # 'form': form,

    }
    return render(request, 'store/cart.html', context)




@login_required(login_url="login")
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += float("{:.2f}".format(cart_item.product.price * cart_item.quantity))
            quantity += cart_item.quantity
        tax = float("{:.2f}".format((20 * total)/100))

        grand_total = float("{:.2f}".format(total + tax))
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)
