from products.models import (Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview,
                             WishList, Address)


def default(request):
    categories = Category.objects.all()

    return {
        'categories': categories,
    }
