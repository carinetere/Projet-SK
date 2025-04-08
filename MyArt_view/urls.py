from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
    path('contact/', views.contact, name = 'contact'),
    path('products/', views.products, name = 'products'),
    path('product-detail/<str:id_product>', views.product_detail, name ='product-detail'),
    path('product-list/', views.product_list, name = 'product-list'),
    path('cart/', views.cart, name = 'cart'),
    path('checkout/', views.checkout, name= 'checkout'),
    path('services/', views.services, name = 'services'),
    path('work-detail/', views.work_detail, name = 'work-detail'),
    path('work/', views.work, name = 'work'),
    path('review/<str:id_product>', views.add_review, name='add_review'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-to-cart/<str:id_product>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
