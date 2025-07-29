from django.contrib import admin
from .models import Product, Image, Category, Favorite

admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Favorite)
