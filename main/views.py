from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .models import Product, Category


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'main/index.html', {
        'categories': categories,
        'products': products,
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
    return render(request, 'main/single.html', {'product': product})



def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматический вход после регистрации
            messages.success(request, 'Вы успешно создали аккаунт')
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request=request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему')
            return redirect('index')
        messages.error(request, 'Неправильный логин или пароль')
    return render(request, 'main/login.html')