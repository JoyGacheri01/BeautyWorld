from django.shortcuts import render, redirect, get_object_or_404
from .models import BaseProduct 
from . models import Product, CartItem
from .models import NewArrival, BestSellers, Discounted, Cleansing, Oil, Treatment, Braiding
from . models import BlogPost, Testimonial, Order, OrderItem
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import logging
from django.contrib import messages

from .models import Message


# Create your views here.
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_price += product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity})

    empty_cart_message = "Your cart is empty." if not cart_items else ""
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'empty_cart_message': empty_cart_message})

logger = logging.getLogger(__name__)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    if product_id in cart:
        cart[product_id] += 1  # Increment quantity if already in cart
    else:
        cart[product_id] = 1  # Add new product to cart

    request.session['cart'] = cart  # Save the updated cart in the session
    messages.success(request, f"Added {product.name} to your cart.")
    return redirect('cart:view_cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})  # Get cart from session (default to empty if not found)

    # Try to remove the product from the cart
    if cart.pop(str(product_id), None):
        request.session['cart'] = cart  # Save the updated cart in the session
        messages.success(request, "Item removed from your cart.")
    else:
        messages.warning(request, "Item not found in your cart.")
    
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

    new_arrivals = NewArrival.objects.filter(category='new_arrival')
    best_sellers = BestSellers.objects.filter(category='best_seller')
    discounted = Discounted.objects.filter(category='discounted')
    cleansing = Cleansing.objects.filter(category='cleansing')
    oil = Oil.objects.filter(category='oil')
    treatment = Treatment.objects.filter(category='treatment')
    braiding = Braiding.objects.filter(category='braiding')
    products = Product.objects.all()

    context = {
        'new_arrivals': new_arrivals,
        'best_sellers': best_sellers,
        'discounted': discounted,
        'cleansing': cleansing,
        'oil': oil,
        'treatment': treatment,
        'braiding': braiding,
        'products':products,
    }


    return render(request, 'products.html', context)

def new_arrivals(request):
    products = NewArrival.objects.filter(category='new_arrival')
    return render(request, 'items/new_arrivals.html', {'products': products})

def discounted(request):
    products = Discounted.objects.filter(category='discounted')
    return render(request, 'items/discounted.html', {'products': products})

def best_seller(request):
    products = BestSellers.objects.filter(category='best_seller')
    return render(request, 'items/best_sellers.html', {'products': products})

def contact(request):
    return render(request, 'contact.html')

def home(request):
    new_arrivals = NewArrival.objects.filter(category='new_arrival')
    best_sellers = BestSellers.objects.filter(category='best_seller')
    discounted = Discounted.objects.filter(category='discounted')

    
    context = {
        'new_arrivals': new_arrivals,
        'best_sellers': best_sellers,
        'discounted': discounted,
    }
    return render(request, 'home.html', context)

def blog_list(request):
    posts = BlogPost.objects.all()  
    testimonials = Testimonial.objects.all()
    return render(request, 'blog.html', {
        'posts': posts,
        'testimonials': testimonials,

    })

def blog_details(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    related_posts = BlogPost.objects.filter(category=blog.category).exclude(id=blog.id)[:5]
    return render(request, 'blog-details.html', {
        'blog': blog,
        'related_posts': related_posts,

    })

def add_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')
        image = request.FILES.get('image')

        if title and content and author:
            blog_post = BlogPost(
                title=title, 
                content=content, 
                author=author, 
                image=image
            )
            blog_post.save()
            messages.success(request, "Blog post created Successfully.")
            return redirect('cart:blog_list')
        else:
            messages.error(request, "Please fill in all the required fields.")
    return render(request, 'add_blog.html')

def update_blog(request, id):
    blog_post = get_object_or_404(BlogPost, id=id)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')
        image = request.FILES.get('image')

        blog_post.title = title
        blog_post.content = content
        blog_post.author = author
        blog_post.image = image

        blog_post.save()
        messages.success(request, "Blog post updated Successfully.")
        return redirect('cart:blog_list')
    return render(request, 'updateBlog.html', {'blog_post': blog_post})

def delete_blog(request, id):
    blog_post = get_object_or_404(BlogPost, id=id)
    blog_post.delete()
    messages.success(request, "Blog post deleted Successfully.")
    return redirect('cart:blog_list')

def search(request):
    query = request.GET.get('q', '')
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
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total_price += product.price * quantity
        cart_items.append({
            'id': product.id,
            'name': product.name,
            'quantity': quantity,
             })
        
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,  

      })


def order_confirmation(request):
    order_details = request.session.get('order_details', {})
    
    return render(request, 'order_confirmation.html', {'order_details': order_details})


def insert_message(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        new_message = Message(
            name=name, 
            email=email,
            subject=subject,
            message=message
        )
        new_message.save()
        messages.success(request, "Thank you for contacting us. We will get back to you soon.")
        return redirect('thank.html')
    
def thank(request):
    return render(request, 'thank.html')

def add_testimony(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        author = request.POST.get('author')

        testimony = Testimonial(
            content=content,
            author=author
        )

        testimony.save()
        messages.success(request, "Thank you for sharing your testimony with us.")
        return redirect('cart:blog_list')
    return render(request, 'add_testimony.html')

def update_testimony(request, id):
    testimony = get_object_or_404(Testimonial, id=id)
    if request.method == 'POST':
        content = request.POST.get('content')
        author = request.POST.get('author')

        testimony.content = content
        testimony.author = author

        testimony.save()
        messages.success(request, "Testimony updated successfully.")
        return redirect('cart:blog_list')
    return render(request, 'update_testimony.html', {'testimony': testimony})

def delete_testimony(request, id):
    testimony = get_object_or_404(Testimonial, id=id)
    testimony.delete()
    messages.success(request, "Testimony deleted successfully.")
    return redirect('cart:blog_list')


