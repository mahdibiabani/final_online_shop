from django.urls import path
from . import views
from .views import CommentCreateView, search_view

app_name = 'products'

urlpatterns = [
    path('', views.index, name='home'),
    path('products/', views.product_list_view, name='product_list'),
    path('products/<pid>/', views.product_detail_view, name='product_detail'),
    path('category/', views.category_list_view, name='category_list'),
    path('category/<cid>/', views.category_product_list_view, name='category_product_list'),
    path('vendor/', views.vendor_list_view, name='vendor_list'),
    path('vendor/<vid>/', views.vendor_detail_view, name='vendor_detail'),
    path('products/tag/<slug:tag_slug>/', views.tags_list_view, name='tags'),


    path('add_review/<int:pid>/', CommentCreateView.as_view(), name='comment_create'),

    path('search/', search_view, name='search'),


]
