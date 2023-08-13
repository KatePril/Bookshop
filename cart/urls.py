from django.urls import path
from .views import *


urlpatterns = [
    path('add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('create/', OrderCreateView.as_view(), name='create_order'),
    path('delete/<int:pk>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
]