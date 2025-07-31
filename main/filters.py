import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Цена от')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Цена до')

    class Meta:
        model = Product
        fields = ['title', 'city', 'price_min', 'price_max']
