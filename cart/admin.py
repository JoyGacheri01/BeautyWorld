from django.contrib import admin
from .models import Product, CartItem, NewArrival, BestSellers, Discounted, Cleansing, Oil, Treatment, Braiding
from . models import BlogPost, Testimonial, Order, OrderItem

# Admin for BaseProduct subclasses
class BaseProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'category')
    search_fields = ('name', 'description')
    list_filter = ('category',)

# Admin for Product (does not have a 'category' field)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'stock')
    search_fields = ('name', 'description')
    list_filter = ('price',)  

# Register models
admin.site.register(Product, ProductAdmin)  
admin.site.register(CartItem)

# Register subclasses of BaseProduct
admin.site.register(NewArrival, BaseProductAdmin)
admin.site.register(BestSellers, BaseProductAdmin)
admin.site.register(Discounted, BaseProductAdmin)
admin.site.register(Cleansing, BaseProductAdmin)
admin.site.register(Oil, BaseProductAdmin)
admin.site.register(Treatment, BaseProductAdmin)
admin.site.register(Braiding, BaseProductAdmin)

admin.site.register(BlogPost)
admin.site.register(Testimonial)
admin.site.register(Order)
admin.site.register(OrderItem)
