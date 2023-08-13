from django.shortcuts import render
from shop.models import Book

# Create your views here.
def about_us(request):
    books = Book.objects.filter(is_best_saled=True)
    return render(request, 'about_us/about_us.html', {'books': books})