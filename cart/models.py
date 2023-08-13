from django.db import models
from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField

from shop.models import Book

# Create your models here.
class Cart(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.book.name} - {self.quantity}'

class Order(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'Is in progress'),
        ('waiting_for_payment', 'Is waiting for payment'),
        ('in_delivery', 'Was sent'),
        ('completed', 'Is completed'),
        ('canceled', 'Was canceled')
    )
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = PhoneNumberField()
    address = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, blank=True, default=STATUS_CHOICES[0][0])
    email = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):  
        return f'Order №{self.id}'
    
    def delete(self):
        for item in self.books.all():
            item.book.quantity += item.quantity
            item.book.save()
        super().delete()
            
    def get_status(self):
        return dict(self.STATUS_CHOICES)[self.status]

class OrderBook(models.Model):
    order = models.ForeignKey(Order, related_name='books', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.book.name} - {self.quantity}'