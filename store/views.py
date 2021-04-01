from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from json import dumps
from django_tables2.export.export import TableExport



from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
import datetime
import csv
import smtplib

from .models import *
from .utils import cookieCart, cartData, guestOrder
from . import forms
from .forms import *
from .filters import OrderFilter, OrderHomeFilter

from .forms import CustomerLoginForm


# Create your views here.



def home(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    category = Category.objects.all()
    properties = SiteProperties.objects.get(purpose="Home Carousel")
    featured = Product.objects.filter(featured=True)
    articles = Article.objects.all().order_by('date')[0:5]
    json_serializer = serializers.get_serializer("json")()
    timer = json_serializer.serialize(Timer.objects.all(), ensure_ascii=False)


    if request.method == "POST": 
        form = NewsletterForm(request.POST)
       
        if form.is_valid():
            instance = form.save(commit = False)
            instance.save()
            return redirect('list')
         
            
    else: 
        form = NewsletterForm()



    products = Product.objects.all()[:5]

    context = {
        'items': items, 'order': order, 'cartItems': cartItems, 
        'products':products, 'articles':articles, 'timer':timer,
        'category':category,'properties':properties,'form':form
    }

    return render(request, "store/boot_home.html", context)

def carousel_detail(request):
    context = {} 
    if request.method == "POST": 
        form = GeeksForm(request.POST, request.FILES) 
        if form.is_valid(): 
            name = form.cleaned_data.get("name") 
            img = form.cleaned_data.get("geeks_field") 
            obj = CarouselData.objects.create( 
                                 body = name,  
                                 image = img 
                                 ) 
            obj.save() 
            print(obj) 
    else: 
        form = GeeksForm() 
    context['form']= form 
    return render(request, "store/carousel_edit.html", context) 

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    category = Category.objects.all()



    products = Product.objects.all()
    # context = {'Products': products}

    #carousel_content = CarouselData.objects.all()

    print(products, cartItems)
    return render(request, 'store/shop.html',
                  {'products': products, 'cartItems': cartItems, 'order':order,'items':items,'category':category})


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    category = Category.objects.all()


    context = {'items': items, 'order': order, 'cartItems': cartItems,'category':category}
    return render(request, 'store/shopping-cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    category = Category.objects.all()

    context = {'items': items, 'order': order, 'cartItems': cartItems,'category':category} 
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def updateGuest_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def email_send():

    email_details = Send_email.objects.all()
    sender_email = "sosahlawe@gmail.com"
    reciever_email = "mantsenii0@gmail.com"
    password = 'Explorer101DogsAreAwesome' #Try putting all these in a form
    message = "Transaction completed! By Lawe Sosah"

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(sender_email,password)
    print("Login success")
    server.sendmail(sender_email,reciever_email,message)
    print("Email has been sent to", reciever_email)

def inventory():
    order = Order.objects.get(order=Order)
    orderitem = OrderItem.objects.get(order=order)
    for item in orderitem():
        product = item.product
        product.num_available = product.num_available - item.quantity
        product.save()

def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderitem = OrderItem.objects.get_or_create(order=order)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    print(total)

    if total == float(order.get_cart_total):
        order.complete = True
        email_send()
        inventory()
        for item in order.get_cart_quantity():
            product = item.product
            product.num_available = product.num_available - item.quantity
            product.save()
            
    order.save()

    

    

    print('total:', total)
    print('order.get_cart_total:', order.get_cart_total)
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )


    return JsonResponse('Payment Complete!', safe=False)


def Search(request):
    data = cartData(request)
    cartItems = data['cartItems']

    kw = request.GET.get("keyword")
    results = Product.objects.filter(
        Q(name__icontains=kw) | Q(price__icontains=kw))
    print(results)

    return render(request, 'store/search.html', {'cartItems': cartItems, 'results': results})


def product_detail(request, slug):
    # return HttpResponse(slug)
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = get_object_or_404(Product, slug=slug)

    reviews = ProductReview.objects.all()
    product = Product.objects.all()[:4]
    stars = ProductReview.objects.count() 

    if request.method == "POST": 
        form = NewsletterForm(request.POST)
       
        if form.is_valid():
            instance = form.save(commit = False)
            instance.save()
            return redirect('list')
         
            
    else: 
        form = NewsletterForm()

    if request.method == 'POST' and request.user.is_authenticated:
        stars = request.POST.get('stars', 3)
        content = request.POST.get('content','')

        review = ProductReview.objects.create(product=products, user=request.user, stars=stars, content=content  )

        return redirect('detail', slug=slug)


    #products = Product.objects.get(slug=slug)
    return render(request, 'store/product.html', {'products': products, 'cartItems': cartItems,'order':order,'items':items,'product':product,'products':products,'reviews':reviews, 'stars':stars,'form':form})


def product_create(request):
    form = CreateProduct()
    if request.method == 'POST':
        form = CreateProduct(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.author = request.user
            instance.save()
            return redirect('store')

    return render(request, 'adminpages/product_create.html', {'form': form})

"""
def create_products(request):
    products = Product.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.files.getlist('images')
        
        if data['product'] != 'none':
            product = Product.objects.get(id=data[product])
        elif data['product_new'] != '':
            product, created = Product.objects.get_or_create(name=data['product_new'])

        else:
            Product = None
        for image in images:
            product = Product.objects.create(

                product = product,
                image = image
            ) 
        return redirect('list')

    return render(request, 'adminpages/product_create.html', {'products':products})
"""

def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = CreateProduct(instance=product)

    if request.method == 'POST':
        form = CreateProduct(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'adminpages/product_create.html', {'form': form})

def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    shipping  = ShippingAddress.objects.get(customer=order.customer)
    qs = OrderItem.objects.filter(order=order)
    

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('admin_home')

    return render(request, 'adminpages/order_create.html', {'form': form,'order':order,'shipping':shipping, 'qs':qs})


def shipping_details(request, pk):
    shipping = ShippingAddress.objects.get(id=pk)


    return render(request, 'adminpages/shipping_details.html',{'shipping':shipping})

def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        product.delete()
        return redirect('admin_home')

    context = {'item': product}
    return render(request, 'adminpages/delete.html', context)


def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('admin_home')

    context = {'item': order}
    return render(request, 'adminpages/delete_order.html', context)


def all_categories(request, pk):
    category = Category.objects.all()
    categories = category.get(id=pk)
    
    products = Product.objects.filter(category=categories)

    return render(request, 'store/categories.html', {'categories': categories, 'products':products,'category':category})




class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("admin_home")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)


def admin_logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('store')


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


def home_admin(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    # Add status model field
    delivered = orders.filter(complete='True').count()
    pending = orders.filter(complete='False').count()


    return render(request, 'adminpages/admin_home_page.html',
                  {'orders':orders, 'total_orders': total_orders, 'delivered': delivered,'pending':pending})


def out_for_delivery(request):
    all_orders = Order.objects.all()
    delivering = all_orders.filter(status="Out for delivery")

    total_orders = all_orders.count()
    delivered = all_orders.filter(complete='True').count()
    pending = all_orders.filter(status='Pending').count()
    context = {'delivering':delivering,'total_orders': total_orders, 'delivered': delivered, "pending": pending }

    return render(request,'adminpages/admin_outfordelivery.html',context)


def delivered(request):
    all_orders = Order.objects.all()
    done = all_orders.filter(status="Delivered")

    total_orders = all_orders.count()
    delivered = all_orders.filter(complete='True').count()
    pending = all_orders.filter(status='Pending').count()
    context = {'done':done,'total_orders': total_orders, 'delivered': delivered, "pending": pending }

    return render(request,'adminpages/admin_delivered.html',context)


def pending_orders(request):
    all_orders = Order.objects.all()
    done = all_orders.filter(status="Delivered")
    pending_orders = all_orders.filter(status="Pending")

    total_orders = all_orders.count()
    delivered = all_orders.filter(complete='True').count()
    pending = all_orders.filter(status='Pending').count()
    context = {'done':done,'total_orders': total_orders, 'delivered': delivered, "pending": pending, 'pending_orders':pending_orders}

    return render(request,'adminpages/admin_pending.html',context)

class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/admin_home_page.html"

    def get(self, request, *args, **kwargs):

        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        all_orders = Order.objects.all()
        pending_orders = Order.objects.filter(status= "Pending")
        qs = OrderItem.objects.all().order_by('order')
        pending = Order.objects.filter(status = "Pending")
        newsletter = Newsletter.objects.all().order_by('date')
        articles = Article.objects.all()


        orders = qs
        orderFilter = OrderHomeFilter(request.GET, queryset=orders) 
        orders = orderFilter.qs



       # total_products = OrderItem.order()


        products = Product.objects.all()
        #order_items = Order.get_cart_items(self)

        customer = Customer.objects.all()




        total_orders = all_orders.count()
        delivered = all_orders.filter(complete='True').count()
        pending = all_orders.filter(status='Pending').count()

        context = {
            "all_orders": all_orders, 'total_orders': total_orders, 
            'delivered': delivered, "pending": pending,"pending_orders":pending_orders,
            'qs':qs,'products':products,'filter':orderFilter,'orders':orders, 'items': items, 'order': order, 'cartItems': cartItems,'newsletter':newsletter,'articles':articles

            
        }
        return render(request, "adminpages/admin_home_new.html", context)


class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/admin_detail.html"
    model = Order
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class admin_ordering(AdminRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        order = Order.objects.all()
        orderitem = OrderItem.objects.all()
        context = {
            "order": order,
            'orderitem':orderitem
            
        }
        return render(request, "adminpages/admin_detail.html", context)




class view_customer(AdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        customers = Customer.objects.order_by('name')
        shipping = ShippingAddress.objects.all()
        orderItem = OrderItem.objects.all()
        context = {
            "customers": customers,
            "shipping":shipping,
            "orderItem":orderItem
        }
        return render(request, "adminpages/customer_view.html", context)


def customer_view_details(request):
   # customer = Customer.objects.get(id=pk)
    customer = Customer.objects.all()
  #  orders = customer.order_set.all()
 #   order = orders.get_cart_items()
    #total_orders = orders.count()

   # orderitems = OrderItem.objects.get(id=pk)
 #   shipping = ShippingAddress.objects.all()

  #  items = data['items']

  #  orderFilter = OrderFilter(request.GET, queryset=orders) 
   # orders = orderFilter.qs


    return render(request, 'adminpages/customer_view_details.html', {'customer':customer})


def detail_cust(request,pk):

   # customer = Customer.objects.get(id=pk)

    data = cartData(request)
    cartItems = data['cartItems']
    #order = Order.objects.get(id=pk)
    items = data['items']
   # ordering = order.get_cart_item()

    orderitems = OrderItem.objects.get(id=pk)
 #   orderitem = orderitems.values('product')
    customer = Customer.objects.all()
    shipping  = ShippingAddress.objects.get(customer=orderitems.order.customer)
    
    orders = orderitems.order



  #  total_orders = orders.count()


  #  ordering = orderitems.orderitem_set.all
    
    return render(request, 'adminpages/cust_details.html', {'orderitems':orderitems,'customer':customer,'shipping':shipping,'orders':orders,'cartItems':cartItems,'items':items,'filter':OrderFilter})


# def customer_view(request):

# customers = Customer.objects.all()

# return render(request,'adminpages/customer_view.html',{'customers':customers})

class admin_products(AdminRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        context = {
            "products": products
        }
        return render(request, "adminpages/products.html", context)

class admin_orders(AdminRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        orderitems = OrderItem.objects.all()
        pending = Order.objects.filter(status="Pending")
        qs = orderitems.order_by('order')

        context = {
            "orders": orders,'qs':qs, 'pending':pending
            
        }
        return render(request, "adminpages/admin_orders.html", context)

def Export(request):
    order = Order.objects.get_or_create(customer=customer, complete=False)

    order_fields = [x.name for x in order.get_cart_item]
    print(order_fields)
    """

    orderitem_fields = [x.name for x in OrderItem._meta.concrete_fields]
    shipping_address_fields = [x.name for x in ShippingAddress._meta.concrete_fields]

    all_fields = order_fields + orderitem_fields + shipping_address_fields
    order_list = list(OrderItem.objects.values_list(*all_fields))

    with open('test_export.csv', 'w', newline='') as myfile:
        for _list in order_list:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(_list)
            """
    """
   response = HttpResponse(content_type ='text/csv')

   writer = csv.writer(response)
   writer.writerow(['customer','date_ordered','complete','No of items','product'])

   rows = []

   order_row = Order.objects.all()
   shipping = ShippingAddress.objects.filter(order=order_row)
   rows.append(order_row)
   rows.append(shipping)

   print(rows)

   


   for order in Order.objects.all().values_list('customer','date_ordered','complete','orderitem'):

       for orderitem in OrderItem.objects.all().values_list('product'):

        writer.writerow(order)
        writer.writerow(orderitem)
        print (Order.customer)
   response['content-Disposition'] = 'attachment; filename="total_orders.csv"'

   return response
"""



def table_export():
    export_format = request.GET.get('_export', None)

    if TableExport.is_valid_format(export_format):
        table = [[Order],[ShippingAddress]]
        exporter = TableExport(export_format, table)
        return exporter.response('File_Name.{}'.format(export_format))


class ClubChartView(TemplateView):
    template_name = 'adminpages/chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = OrderItem.objects.all() 
        return context



class AdminProductCreateView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/product_create.html"
    form_class = CreateProduct
    success_url = reverse_lazy("admin_home")

    def form_valid(self, form):
        p = form.save()
        return super().form_valid(form)
        
class AdminProductEdit(AdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.all()
        form = UpdateProduct(instance = product)

        if request.method == 'POST':
            form = forms.UpdateProduct(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/')
        context = {
            'product':product,
            'form':form
        }
        return render(request, "adminpages/product_create.html", context)


def Properties(request):
    properties = SiteProperties.objects.get(purpose="Home Carousel")

    context = {

        'properties':properties
    }

    return render(request,'adminpages/edit_site_properties.html',context)

def update_article(request,pk):
    article = Article.objects.get(id=pk)
    form=forms.UpdateArticle(instance=article)

    if request.method == 'POST':
        form = forms.UpdateArticle(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    return render(request, 'adminpages/update_article.html', {'form': form,'article':article})
#send_email()


def article_list(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    articles = Article.objects.all().order_by('date')#[0:20]
    about = Admin.objects.all()
    recent = Article.objects.all().order_by('date')[0:5]
    categories = Category.objects.all()

    paginator = Paginator(articles,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    
    
    #carousel_info = Carousel.objects.filter(purpose="Homepage")

    #num_visits = request.session.get('num_visits', 0)
    #request.session['num_visits'] = num_visits + 1

    return render(request, 'store/blog.html', {'articles': articles,'data': data, 'cartItems':cartItems,'order':order, 'items':items,'about':about, 'recent':recent, 'page_obj':page_obj, 'category':categories})


#For comparison
class PostListView(ListView):
    model = Article
    template_name = 'store/blog.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Article
    template_name = 'store/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_query_set(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Article.objects.filter(author=user).order_by('-date')


def article_detail(request, slug):
    # return HttpResponse(slug)
    # article = Article.objects.get(slug=slug)
    by = Admin.objects.all()
    article = Article.objects.all()
    articles = get_object_or_404(Article, slug=slug)
    about = by.filter(full_name='Lawe Sosah')

    

    articles.page_views = articles.page_views+1
    articles.save()
    comments = articles.comments.filter(active=True)
    new_comment = None

    paginator = Paginator(article,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Comment posted
    if request.method == 'POST':
        comment_form = CreateComment(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
             #Assign the current post to the comment
            new_comment.article = articles
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CreateComment()

    return render(request, 'store/blog-details.html', {'article': articles,'about':about, 'form':comment_form,'comments':comments,'new_comment':new_comment, 'views':articles.page_views, 'page_obj':page_obj})


def newsletter_signup(request):
    context = {} 
    if request.method == "POST": 
        form = NewsletterForm(request.POST)
       
        if form.is_valid():
            instance = form.save(commit = False)
            instance.save()
            return redirect('list')
         
            
    else: 
        form = NewsletterForm()
    context['form']= form

    return render(request, "adminpages/newsletter_signup.html", context) 
