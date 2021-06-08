from django.contrib import admin
from django.urls import path,include,re_path
from .import views
from .views import *

urlpatterns = [

    path('',views.home, name="home"),

    path('store/',views.store, name="store"),


     path('about/', views.about_us, name="about"),



     path("shipping_details/<int:pk>/", views.shipping_details,
         name="shipping_details"),
    path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),

    path('admin-customer/', views.view_customer.as_view(), name="customer"),

    path("admin-home/", AdminHomeView.as_view(), name="admin_home"),

    path("admin-logout/", admin_logout_view, name="admin_logout"),

    path("admin-products/", admin_products.as_view(), name="admin_products"),

    path("admin-orders/", admin_orders.as_view(), name="admin_orders"),

    path("admin-delivering/", views.out_for_delivery, name="delivering"),

    path("admin-delivered/", views.delivered, name="delivered"),

    path("admin-pending/", views.pending_orders, name="pending"),

    path('new_orders/<str:pk>/', views.new_order, name="new_orders"),


    path('update_item/', views.updateItem, name="update_item"),
    path('update_guest_item/', views.updateGuest_item, name="update_item"),

    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('blog/', views.article_list, name="list"),
    path('products/category/<str:pk>/', views.all_categories, name="category"),

     path('blog/article_details/<slug:slug>/', views.article_detail, name="article_details"),

    path("posts/<str:username>", UserPostListView.as_view(), name="user-posts"),




   # re_path(r'^(?P<slug>[\w-]+)/$', views.product_detail, name='detail'),
    path('product_details/<slug:slug>/', views.product_detail, name="detail"),

   # re_path(r'^(?P<slug>[\w-]+)/$', views.article_detail, name='article_details'),






    path('process_order/', views.process_order, name="process_order"),



#     path('create/', views.AdminProductCreateView.as_view(), name="create"),

    path('create/', views.AdminProductCreateView.as_view(), name="create"),


    path('carousel_edit/', views.carousel_detail, name="carousel"),

    path('update_product/<str:pk>/', views.update_product, name="update_product"),


    path('update_order/<str:key>/', views.update_order, name="update_order"),

    path('customer_details/', views.customer_view_details, name="customer_details"),

    path('export/', views.Export, name="export"),

    #path('update_order/<str:key>/', views.update_order, name="update_order"),

    path('delete_order/<str:pk>/', views.delete_order, name="delete_order"),

    path('delete_product/<str:pk>/', views.delete_product, name="delete_product"),


    







    path('search/', views.Search, name="search"),

    path('chart/', views.ClubChartView.as_view(), name="chart"),



    path("cust_details/<int:pk>/", views.detail_cust,
         name="cust_details"),

    #re_path(r'^(?P<slug>[\w-]+)/$', views.detail_cust, name='cust_details'),


    #re_path(r'^(?P<slug>[\w-]+)/$', views.admin_ordering, name='ordering'),

    

    #re_path(r'^(?P<slug>[\w-]+)/$', views.updateOrder, name='update_order'),

    path("admin-order/<int:pk>/", admin_ordering.as_view(),
         name="admindetail"),

     path("newsletter-signup/",views.newsletter_signup, name="newsletter"),

     path('aboutus/',views.about_us, name="about")

        #Excel Stuff
    


]