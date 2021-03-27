from django import forms
from store.models import CarouselData, Product, Order, Category, OrderItem, Newsletter, Comments


class CarouselForm(forms.ModelForm):
    class Meta:
        model = CarouselData

        fields = ['body', 'image']

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-group row'}),

            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),


        }


class CreateProduct(forms.ModelForm):
    """more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))
    """
    class Meta:
        model = Product

        fields = ['name', 'price','category', 'digital', 'image' , 'description', 'slug']

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-group row'}),
            'price': forms.TextInput(attrs={'class': 'form-group row'}),
           # 'category': forms.TextInput(attrs={'class': 'form-group row'}),
            'digital': forms.CheckboxInput(attrs={'class': 'form-group row'}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control","multiple": True}),
            'description': forms.Textarea(attrs={'class': 'form-group row'}),
            'slug': forms.TextInput(attrs={'class': 'form-group row'}),

        }

class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['quantity','Product','complete']

class UpdateProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class GeeksForm(forms.Form): 
    name = forms.CharField() 
    geeks_field = forms.ImageField() 

class CreateComment(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['name','email','comment']

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = '__all__'

        exclude = ['date']




