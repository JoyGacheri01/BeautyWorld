from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product/')
    stock = models.PositiveIntegerField(default=0)  # Added this here

    def __str__(self):
        return self.name
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)

    class Meta:
        unique_together = ('product', 'user')

# Abstract BaseProduct for common fields
class BaseProduct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=255)

    
    class Meta:
        abstract = True  # This makes the model abstract so it won't create a separate table

    def __str__(self):
        return self.name

# Specific Product Types
class NewArrival(BaseProduct):
    CATEGORY = "new_arrival"
    category = models.CharField(max_length=20, default=CATEGORY, editable=False)

class BestSellers(BaseProduct):
    CATEGORY = "best_seller"
    category = models.CharField(max_length=20, default=CATEGORY, editable=False)

class Discounted(BaseProduct):
    CATEGORY = "discounted"
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, default=CATEGORY, editable=False)

class Cleansing(BaseProduct):
    CATEGORY = "cleansing"
    category = models.CharField(max_length=20, default=CATEGORY, editable=False)

class Oil(BaseProduct):
    CATEGORY = "oil"
    category = models.CharField(max_length=20, default=CATEGORY, editable=False)

class Treatment(BaseProduct):
    CATEGORY = "treatment"
    category = models.CharField(max_length=20, default=CATEGORY, editable=False)

class Braiding(BaseProduct):
    CATEGORY = "braiding"
    category = models.CharField(max_length=20, default=CATEGORY, editable=False)


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    date_published = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    excerpt = models.TextField(max_length=300, blank=True)  # For blog post preview

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial by {self.author}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="pending")
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='Not specified')
    transaction_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"
    

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name