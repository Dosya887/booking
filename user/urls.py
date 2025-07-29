from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import login_view, confirm_2fa_view


urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', login_view, name='login'),
    path('confirm/', confirm_2fa_view, name='confirm_2fa'),
]