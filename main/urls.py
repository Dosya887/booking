from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('single/<int:product_id>/', views.single_view, name='single_view'),
    path('category/<int:category_id>/', views.category_view, name='category'),

]