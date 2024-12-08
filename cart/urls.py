from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.home, name='home'),
    path('product/', views.product, name='product'),
    path('cart/', views.view_cart, name='view_cart'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('new_arrivals/', views.new_arrivals, name='new_arrivals'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:blog_id>/', views.blog_details, name='blog_details'),
    path('discounted/', views.discounted, name='discounted'),
    path('best_seller/', views.best_seller, name='best_seller'),
    path('search/', views.search, name='search'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('insert_message/', views.insert_message, name="insert_message"),
    path('thank/', views.thank, name="thank"),
    path('checkout/', views.checkout, name='checkout'),


]