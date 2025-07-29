from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import CustomUserCreationForm
from .utils import send_2fa_code
from django.contrib import messages


from .models import Email2FACode


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
    return render(request, 'user/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            request.session['pre_2fa_user_id'] = user.id
            send_2fa_code(user)
            return redirect('confirm_2fa')
        else:
            messages.error(request, 'Неверные учетные данные')

    return render(request, 'user/login.html')


def confirm_2fa_view(request):
    user_id = request.session.get('pre_2fa_user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(get_user_model(), id=user_id)
    if request.method == 'POST':
        code_input = request.POST['code']
        twofa = Email2FACode.objects.filter(user=user).first()
        if twofa and not twofa.is_expired() and twofa.code == code_input:
            login(request, user)
            del request.session['pre_2fa_user_id']
            twofa.delete()
            return redirect('index')
        else:
            messages.error(request, 'Неверный или просроченный код')

    return render(request, 'user/confirm_2fa.html', {'email': user.email})