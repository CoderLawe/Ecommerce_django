from django.contrib import admin
from django.urls import path,include,re_path
from .import views
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup_view, name="signup"),

]