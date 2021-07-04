import datetime
from django.contrib import admin
from django.urls import reverse
from .models import *

# Register your models here.

def admin_order_shipped(ModelAdmin, request, queryset):
    for order in queryset:
      #  order.shipping = datetime.datetime.now()
        order.status = 'Delivered'
        order.save()
    return
admin_order_shipped.short_description = 'Set shipped'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_filter = ['date_ordered','status']
    search_fields= ['customer']
    inlines = [OrderItemInline]
    actions = [admin_order_shipped]

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
       model = Product

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Customer)
# admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(CarouselData)
admin.site.register(Admin)
admin.site.register(Category)
admin.site.register(Send_email)
admin.site.register(Article)
admin.site.register(Newsletter)
admin.site.register(Comments)
admin.site.register(Timer)
admin.site.register(ProductReview)
admin.site.register(SiteProperties)
# admin.site.register(ProductImage)
admin.site.register(Order_customer)





