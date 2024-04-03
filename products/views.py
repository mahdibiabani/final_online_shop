from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from taggit.models import Tag
from products.forms import ProductReviewForm
from django.views import generic
from django.contrib import messages
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
    reviews = ProductReview.objects.filter(product=product).order_by('-date_created')
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    review_form = ProductReviewForm()
    product_image = product.product_images.all()

    context = {
        "product": product,
        "review_form": review_form,
        "product_image": product_image,
        "products": products,
        "reviews": reviews,
        'average_rating': average_rating,
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


# def add_review(request, pid):
#     product = Product.objects.get(pk=pid)
#     user = request.user
#
#     review = ProductReview.objects.create(
#         user=user,
#         product=product,
#         review=request.POST['review'],
#         rating=request.POST['rating'],
#     )
#
#     context = {
#         'user': user.username,
#         'review': request.POST['review'],
#         'rating': request.POST['rating'],
#
#     }
#
#     average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
#
#     return JsonResponse(
#         {
#             'bool': True,
#             'context': context,
#             'average_rating': average_rating,
#         }
#     )

class CommentCreateView(generic.CreateView):
    model = ProductReview
    form_class = ProductReviewForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user

        pid = int(self.kwargs['pid'])
        product = get_object_or_404(Product, pid=pid)
        obj.product = product

        messages.success(self.request, 'Comment successfully created')
        return super().form_valid(form)


def search_view(request):
    query = request.GET.get('q')
    products = Product.objects.filter(title__icontains=query).order_by('-date_created')

    context = {
        "products": products,
        "query": query,
    }

    return render(request, 'products/search.html', context)
