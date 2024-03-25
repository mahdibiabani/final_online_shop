from django.shortcuts import render
from django.views.generic import TemplateView

from products.models import (Product, Category, Vendor, CartOrder, CartOrderItems,
                             ProductImages, ProductReview, WishList, Address)


def index(request):
    products = Product.objects.filter(product_status="published", featured=True)
    context = {
        'products': products
    }
    return render(request, 'products/home.html', context)


def product_list_view(request):
    products = Product.objects.filter(product_status="published")

    context = {
        "products": products
    }
    return render(request, 'products/product-list.html', context)


def category_list_view(request):
    categories = Category.objects.all()

    context = {
        "categories": categories
    }
    return render(request, 'products/category-list.html', context)
