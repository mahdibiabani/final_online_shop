from django.shortcuts import render
from django.views.generic import TemplateView

from products.models import (Product, Category, Vendor, CartOrder, CartOrderItems,
                             ProductImages, ProductReview, WishList, Address)


def index(request):
    products = Product.objects.all()
    context ={
        'products': products
    }
    return render(request, 'products/home.html', context)