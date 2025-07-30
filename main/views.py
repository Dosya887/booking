from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Favorite


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    return render(request, 'main/index.html', {
        'categories': categories,
        'products': products,
        'favorite_ids': favorite_ids,
        'selected_category': None,  # Для выделения активной кнопки
    })

def category_view(request, category_id):
    categories = Category.objects.all()
    selected_category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=selected_category)
    return render(request, 'main/index.html', {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,  # Покажем активную категорию
    })


def single_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    recommendations_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    product_like = Favorite.objects.filter(product=product).count()
    return render(request, 'main/single.html', {
        'product': product,
        'recommendations_products': recommendations_products,
        'product_like': product_like,
    })

@login_required
def favorite_product_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'main/favorite.html', {'favorites': favorites})

def like_product_view(request, product_id):

    if not request.user.is_authenticated:
        messages.error(request, 'Войдите в систему')
        return redirect('index')

    product = get_object_or_404(Product, id=product_id)
    like_product = Favorite.objects.filter(user=request.user, product=product).first()
    if not like_product:
        Favorite.objects.create(user=request.user, product=product)

    else:
        like_product.delete()

    return redirect('index')
