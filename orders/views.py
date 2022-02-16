from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


# def payments(request):
#     body = json.loads(request.body)
#     order = Order.objects.get(user=request.user, is_ordered=False, order_number=body["orderID"])
#     # store transaction details
#     payment = Payment(
#         user = request.user,
#         payment_id = body['transID'],
#         payment_method = body['payment_method'],
#         amount_paid = order.order_total,
#         status = body['status']
#     )
#     payment.save()
#
#     order.payment = payment
#     order.is_ordered = True
#     order.save()
#
#     #move cart items to Order Product table
#     cart_items = CartItem.objects.filter(user=request.user)
#
#     for item in cart_items:
#         orderproduct = OrderProduct()
#         orderproduct.order_id = order.id
#         orderproduct.payment = payment
#         orderproduct.user_id = request.user.id
#         orderproduct.product_id = item.product_id
#         orderproduct.quantity = item.quantity
#         orderproduct.product_price = item.product.price
#         orderproduct.ordered = True
#         orderproduct.save()
#
#     #reduce quantity of sold products
#         product = Product.objects.get(id=item.product_id)
#         product.stock -=item.quantity
#         product.save()
#     #clear cart
#     CartItem.objects.filter(user=request.user).delete()
#
#     #send order number and transaction id to sendData method
#
#
#
#
#     mail_subject = 'thank you for order'
#     message = render_to_string('orders/order_recieved_email.html', {
#         'user': request.user,
#         'order': order,
#
#     })
#     to_email = request.user.email
#     send_email = EmailMessage(mail_subject, message, to=[to_email])
#     send_email.send()
#
#     data = {
#         'order_number': order.order_number,
#         'transID': payment.payment_id,
#     }
#     return JsonResponse(data)


def payments(request):
    pass

def place_order(request, total=0, quantity=0):
    current_user = request.user

    #if cart count 0
    cart_items =  CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    total = 0
    for cart_item in cart_items:
        total += float("{:.2f}".format(cart_item.product.price * cart_item.quantity))
        quantity += cart_item.quantity
    tax = float("{:.2f}".format((20 * total)/100))
    grand_total = float("{:.2f}".format(total + tax))

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            #store all information
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.organization = form.cleaned_data['organization']
            data.ico = form.cleaned_data['ico']
            data.dic = form.cleaned_data['dic']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.post_code = form.cleaned_data['post_code']
            data.post_first_name = form.cleaned_data['post_first_name']
            data.post_last_name = form.cleaned_data['post_last_name']
            data.post_organization = form.cleaned_data['post_organization']
            data.post_address_line_1 = form.cleaned_data['post_address_line_1']
            data.post_address_line_2 = form.cleaned_data['post_address_line_2']
            data.post_country = form.cleaned_data['post_country']
            data.post_city = form.cleaned_data['post_city']
            data.post_post_code = form.cleaned_data['post_post_code']
            data.order_note = form.cleaned_data['order_note']
            data.total = total
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.shipping_method = form.cleaned_data['shipping_method']
            data.save()
            #generate order id
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            shipping = 0
            if order.shipping_method == "Kurier":
                shipping = float(4)
            elif order.shipping_method == "Dobierka":
                shipping = float(5.5)
                if data.post_country == 'Česká Republika':
                    shipping += float(2)
            else:
                shipping = 0
            grand_total = float("{:.2f}".format(total + tax + shipping))
            data.shipping_price = shipping
            data.order_total = grand_total
            data.save()

            #payment = Payment.objects.get(user=current_user)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'shipping': shipping,
                'grand_total': grand_total,
                #'payment': payment,
            }
            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')


def order_complete(request):

    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += float("{:.2f}".format(i.product_price * i.quantity))

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
            'shipping': order.shipping_price,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')


def order_complete_dobierka(request, order_num):
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_num)
    # store transaction details
    payment = Payment(
        user = request.user,
        payment_id = "0",
        payment_method = "Dobierka",
        amount_paid = order.order_total,
        status = "Dobierka"
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    #move cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

    #reduce quantity of sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -=item.quantity
        product.save()
    #clear cart
    CartItem.objects.filter(user=request.user).delete()
    #send order number and transaction id to sendData method
    order = Order.objects.get(is_ordered=True, order_number=order_num)
    #email to customer
    mail_subject = 'Ďakujeme za Vašu objednávku'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,

    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    #email to shop
    mail_subject = 'Máte novú objednávku'
    message = render_to_string('orders/order_recieved_email_to_shop.html', {
        'order': order,

    })
    to_email = "objednabky@elele.com"
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()



    try:
        order = Order.objects.get(order_number=order_num, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += float("{:.2f}".format(i.product_price * i.quantity))


        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,

        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
