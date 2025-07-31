from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('single/<int:product_id>/', views.single_view, name='single_view'),
    path('category/<int:category_id>/', views.category_view, name='category'),
    path('like_product/<int:product_id>/', views.like_product_view, name='like_product'),
    path('favorites/', views.favorite_product_view, name='favorites'),
    path('filter/', views.product_list_view, name='filter'),
]