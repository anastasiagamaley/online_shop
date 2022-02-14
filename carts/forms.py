from django import forms
from .models import CartItem


class QuantityForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ('quantity',)
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
