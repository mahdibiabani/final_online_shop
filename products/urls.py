from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='home'),
    path('category/', views.category_list_view, name='category_list'),
    path('products/', views.product_list_view, name='product_list'),
]