from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from taggit.models import Tag

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


def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(status="published", category=category)

    context = {
        "products": products,
        "category": category
    }

    return render(request, 'products/category-product-list.html', context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors": vendors
    }
    return render(request, 'products/vendor-list.html')


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    context = {
        "vendor": vendor
    }
    return render(request, 'products/vendor-detail.html', context)


def product_detail_view(request, pid):
    product = get_object_or_404(Product, pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)
    product_image = product.product_images.all()

    context = {
        "product": product,
        "product_image": product_image,
        "products": products
    }
    return render(request, 'products/product-detail.html', context)


def tags_list_view(request, tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by('-id')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

        context = {
            "products": products
        }
        return render(request, 'products/tag.html', context)
