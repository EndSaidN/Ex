from django.contrib import admin
from mahsulotlar.models import Product
from mahsulotlar.models import Category
from akkauntlar.models import Customer
from akkauntlar.models import Orders


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class OrdersAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'price', 'address', 'status']


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer)
admin.site.register(Orders, OrdersAdmin)