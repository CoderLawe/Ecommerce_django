from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from tinymce.models import HTMLField





# Create your models here.


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(blank=True ,null=True)
    mobile = models.CharField(max_length=20)
    bio = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.full_name

class Send_email(models.Model):
    email  = models.EmailField()
    password = models.CharField(max_length=200)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

    @property
    def orders(self):
        order_count = self.order_set.all().count()
        ind_orders = self.order_set.all()
        #ind_orderings = ind_orders.get(ind_orders)
        return (ind_orders)

    def shipping(self):
        shipping = self.order_set.all()
        address = shipping

        return(address)

   
    

class Category(models.Model):
    CATEGORIES = (
        ('Phones', 'Phones'),
        ('Computers', 'Computers'),
        ('Accesories', 'Accesories'),

    )

    title = models.CharField(max_length=200,default = 'Gen')
    slug = models.SlugField(unique=True)


    def __str__(self):
        return self.title




class Product(models.Model):

    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    digital = models.BooleanField(default=False, null=True, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank = True,upload_to = 'images/')
    description = models.TextField()
    detailed_description = models.TextField(null=True, blank="True")
    slug = models.SlugField(default=None)
    featured  = models.BooleanField(default=False)
    created_by = models.ForeignKey(Admin,on_delete= models.CASCADE,related_name='product_posts',default='')
    num_available = models.IntegerField(default=1)
    #addedby = models.ForeignKey(User,on_delete= models.CASCADE,related_name='blog_posts',null = True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        
        url = self.image.url

     
        return url


    def get_rating(self):
        
        total = sum(int(review ['stars']) for review in self.reviews.values())

        if self.reviews.count() > 0:
            return total / self.reviews.count()
        else:
            return 0


    def short_description(self):
        return self.description[:50] +'...'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete = models.CASCADE)
    image = models.ImageField(null=True, blank = True,upload_to = 'images/')


    


class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User,related_name='reviews', on_delete=models.CASCADE)

    content = models.TextField(blank=True, null=True)
    stars = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

   


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    body = HTMLField(blank=True, null=True)
    page_views = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    thumb = models.ImageField(null=True, blank = True,upload_to = 'images/')
    author = models.ForeignKey(User,on_delete= models.CASCADE,related_name='blog_posts',default='')

    def __str__(self):
        return self.title

    def short_title(self):
        return self.title[:20] +'...'


class Timer(models.Model):
    date = models.DateTimeField()

    def __str(self):
        return self.date
    
class Comments(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments',null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length = 200)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']   

    def __str__(self):
        return self.name

    def snippet(self):
        return self.comment[:50] + '...'

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    status = models.CharField(max_length=200, null=True, choices=STATUS, default='Pending')
    

    def __str__(self):
        return str(self.id) + " " + str(self.customer)

    @property
    def shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()

        for i in orderItems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        print (total)
        return total

    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def get_cart_item(self):
        orderitems = self.orderitem_set.all()
        name = [item.product.name for item in orderitems]
        print(name)
        return name

    def get_cart_quantity(self):
        orderitems = self.orderitem_set.all()
        quantity = [item.quantity for item in orderitems]
        return quantity

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    
    date_added = models.DateTimeField(auto_now_add=True)

#Maybe add customer field?

    # def __str__(self):
    #     return self.quantity

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

   

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.address


class CarouselData(models.Model):
    body = models.TextField()
    image = models.ImageField( blank=True, default="placeholder.png")

    def __str__(self):
        return self.body



class Newsletter(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)
    message= models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class SiteProperties(models.Model):
    PURPOSE = (
        ('Home Carousel', 'Home Carousel'),
        ('Home Banner A', 'Home Banner A'),
        ('Home Banner B', 'Home Banner B'),
    )
    title = models.CharField(max_length=200, blank=True, null=True, default='placeholder text')
    body = models.TextField(null=True, blank=True, default='placeholder text')
    aux_text_field = models.TextField(null=True, blank = True, default='placeholder text')
    image = models.ImageField(null=True, blank = True,upload_to = 'images/')
    purpose = models.CharField(max_length=200, choices=PURPOSE)

    def __str__(self):
        return self.purpose

    
