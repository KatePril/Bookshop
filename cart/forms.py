from django import forms
from .models import Cart, Order

class AddCartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'