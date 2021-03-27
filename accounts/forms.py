from django import forms
from store.models import Customer


class CustomerSignup(forms.ModelForm):
    class Meta:
        model = Customer
        User = Customer.name
        fields = ['name','email']