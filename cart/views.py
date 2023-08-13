from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.views.generic import View

from config.settings import PAGE_NAMES

from .forms import AddCartForm, OrderCreateForm
from .models import Cart, Order, OrderBook
from shop.models import Book

# Create your views here.
def get_cart_data(user_id):
    cart = Cart.objects.filter(user=user_id)
    total = 0
    for row in cart:
        total += row.book.price * row.quantity
    return {'cart': cart, 'total': total}

class AddToCartView(LoginRequiredMixin, View):
    def get(self, request):
        data = request.GET.copy()
        data.update(user=request.user)
        request.GET = data
        form = AddCartForm(request.GET)
        
        if form.is_valid():
            cd = form.cleaned_data
            # print(Cart.objects.filter(book=cd['book'], user=cd['user']))
            row = Cart.objects.filter(book=cd['book'], user=cd['user']).first()
            if row:
                row.quantity = cd['quantity']
                book = Book.objects.filter(id=cd['book'].id).first()
                Book.objects.filter(id=cd['book'].id).update(quantity=book.quantity-cd['quantity'])
                row.save()
            else:
                form.save()
            return render(request, 'cart/added.html', {'book': cd['book'], 'cart': get_cart_data(cd['user']), 'breadcrumbs': self.get_breadcrumbs()})
        
    def get_breadcrumbs(self):
        breadcrumbs = {reverse('catalog'): PAGE_NAMES['catalog']}
        breadcrumbs[reverse('cart')] = 'Cart'
        # breadcrumbs[reverse('current')] = 'Added'
        return breadcrumbs
    
class CartView(LoginRequiredMixin, View):
    def get(self, request):
        user_id = request.user.id
        return render(request,
                        'cart/cart_list.html',
                        {'cart': get_cart_data(user_id),
                        'breadcrumbs': self.get_breadcrumbs()})

    def get_breadcrumbs(self):
        breadcrumbs = {reverse('catalog'): PAGE_NAMES['catalog']}
        breadcrumbs['current'] = 'Cart'
        return breadcrumbs


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        print('here GET')
        error = None
        user = request.user
        cart = get_cart_data(user.id)

        if not cart['cart']:
            error = 'Cart is empty'
            messages.error(request, error, extra_tags='danger')
            return redirect(reverse('cart'))
        
        form = OrderCreateForm(data={
            'first_name': user.first_name if user.first_name else '',
            'last_name': user.last_name if user.last_name else '',
            'email': user.email if user.email else '',
            'phone': user.phone if user.phone else '',
            'address': user.address if user.address else '',
        })

        return render(request, 'cart/order_create.html', {'form': form, 'cart': cart, 'error': error, 'breadcrumbs': self.get_breadcrumbs()})
            
    def post(self, request):
        print('here POST')
        user = request.user
        cart = get_cart_data(user.id)
        
        data = request.POST.copy()
        data.update(user=user.id)
        data.update(total=cart['total'])
        data.update(pnohe=user.phone)
        data.update(address=user.address)
        data.update(paid=False)
        print(dict(data))
        request.POST = data
        form = OrderCreateForm(request.POST)
        print(form.errors)
        # print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            order = form.save()
            
            with transaction.atomic():
                for row in cart['cart']:
                    quantity = row.quantity if row.quantity < row.book.quantity else row.book.quantity
                    OrderBook.objects.create(
                        order=order,
                        book=row.book,
                        price=row.book.price,
                        quantity=quantity
                    )
                    Book.objects.filter(id=row.book.id).update(quantity=row.book.quantity - quantity)
                Cart.objects.filter(user=user.id).delete()
            return render(request,
                            'cart/order_created.html',
                            {'order': order, 'breadcrumbs': self.get_breadcrumbs()})
        else:
            messages.error(request, 'Error happened', extra_tags='danger')

        return render(request, 'cart/order_create.html', {'form': form, 'cart': cart, 'breadcrumbs': self.get_breadcrumbs()})
    
    
    def get_breadcrumbs(self):
        breadcrumbs = {reverse('catalog'): PAGE_NAMES['catalog'], reverse('cart'): 'Cart'}
        breadcrumbs['current'] = 'Make order'
        return breadcrumbs

class DeleteFromCartView(LoginRequiredMixin, View):
    def get(self, request, pk):
        get_object_or_404(Cart, user=request.user.id, book=pk).delete()
        return redirect(reverse('cart'))