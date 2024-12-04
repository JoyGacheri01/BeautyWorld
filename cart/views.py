from django.shortcuts import render, redirect, get_object_or_404
from .models import BaseProduct 
from . models import Product, CartItem
from .models import NewArrival, BestSellers, Discounted, Cleansing, Oil, Treatment, Braiding
from . models import BlogPost, Testimonial, Order, OrderItem
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def view_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price* item.quantity for item in cart_items)
    else:
        cart_items = []
        total_price = 0
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:view_cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart:view_cart')



def product(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})



def product_detail(request, product_id):
    product = get_object_or_404(BaseProduct, id=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products.html', context)

def product(request):

    products = NewArrival.objects.filter(category='new_arrival')
    products = BestSellers.objects.filter(category='best_seller')
    products = Discounted.objects.filter(category='discounted')
    products = Cleansing.objects.filter(category='cleansing')
    products = Oil.objects.filter(category = 'oil')
    products = Treatment.objects.filter(category='treatment')
    products = Braiding.objects.filter(category='braiding')


    return render(request, 'products.html', {'products': products})

def new_arrivals(request):
    products = NewArrival.objects.filter(category='new_arrival')
    return render(request, 'items/new_arrivals.html', {'products': products})

def discounted(request):
    products = NewArrival.objects.filter(category='new_arrival')
    return render(request, 'items/discounted.html', {'products': products})

def best_seller(request):
    products = BestSellers.objects.filter(category='new_arrival')
    return render(request, 'items/discounted.html', {'products': products})

def contact(request):
    return render(request, 'contact.html')

def home(request):
    return render(request, 'home.html')


def blog_list(request):
    posts = BlogPost.objects.all()  
    testimonials = Testimonial.objects.all() 
    return render(request, 'blog.html', {
        'posts': posts,
        'testimonials': testimonials
    })

def blog_details(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    related_posts = BlogPost.objects.filter(category=blog.category).exclude(id=blog.id)[:5]
    return render(request, 'blog-details.html', {
        'blog': blog,
        'related_posts': related_posts
    })

def search(request):
    query = request.GET.get('search', '')
    results = []
    if query:
        
        product_results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

        # Search in specific product categories
        new_arrival_results = NewArrival.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
        )
        best_seller_results = BestSellers.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
        )
        discounted_results = Discounted.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
        )
        cleansing_results = Cleansing.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
        )
        oil_results = Oil.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
        )
        treatment_results = Treatment.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
        )
        braiding_results = Braiding.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
        )

        # Combine all search results into one list
        results = list(product_results) + list(new_arrival_results) + list(best_seller_results) + \
            list(discounted_results) + list(cleansing_results) + list(oil_results) + \
            list(treatment_results) + list(braiding_results)
    return render(request, 'results.html', {'results': results, 'query': query})

def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user, is_ordered=False)

    if not cart_items:
        return redirect('cart:product')
    
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
    )
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price = item.product.price
        )
        item.is_ordered = True
        item.save()
    return render(request, 'order.html', order_id= order.id)

def order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'ordery.html', {
        'order': order
    })

def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    order.status = 'Completed'
    order.save()
    CartItem.objects.filter(user=request.user, is_ordered=False).delete()
    return render(request, 'order_confirmation.html', {'order': order})