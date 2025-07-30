from django.contrib import admin
from .models import Product, Image, Category, Favorite
from user.models import Feedback, FeedbackResponse

admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Favorite)
admin.site.register(Feedback)
admin.site.register(FeedbackResponse)