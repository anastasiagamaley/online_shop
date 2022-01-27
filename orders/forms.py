from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'organization', 'ico', 'dic', 'post_code', 'address_line_1', 'address_line_2', 'country', 'city', 'order_note', 'post_first_name', 'post_last_name', 'post_organization', 'post_address_line_1', 'post_address_line_2', 'post_city', 'post_post_code', 'post_country']
