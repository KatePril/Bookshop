from django.contrib import admin
from .models import Order, OrderBook
# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created_at', 'updated_at']
    list_filter= ['user', 'status', 'created_at', 'updated_at']
    list_editable = ['status']
    search_fields = ['id', 'user', 'status', 'created_at', 'updated_at']

@admin.register(OrderBook)
class OrderBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'book', 'price', 'quantity']
    list_filter = ['order', 'book', 'price', 'quantity']
    list_editable = ['price', 'quantity']
    search_fields = ['id', 'order', 'book', 'price', 'quantity']