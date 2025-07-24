from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True, verbose_name='Аватар')
    role = models.CharField(max_length=123, verbose_name='Роль')
    balance = models.PositiveIntegerField(default=0, verbose_name='Баланс')
    email = models.EmailField(verbose_name='Почта')

    def __str__(self):
        return self.username


class City(models.Model):
    title = models.CharField(max_length=123, verbose_name='Название города')

    def __str__(self):
        return self.title


class District(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город', related_name='districts')
    title = models.CharField(max_length=123, verbose_name='Название района')

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=123, verbose_name='Категория')

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='products')
    title = models.CharField(max_length=123, verbose_name='Название')
    area = models.CharField(max_length=123, verbose_name='Площадь')
    geo = models.CharField(max_length=123, verbose_name='Геолокация')
    price = models.PositiveIntegerField(verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    promo_video = models.URLField(verbose_name='Промо-видео')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    image = models.ImageField(upload_to='media/image_view', null=True, blank=True, verbose_name='Фото')

    def __str__(self):
        return self.title


class Image(models.Model):
    file = models.ImageField(upload_to='image', null=True, blank=True, verbose_name='Изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='images')
    is_main = models.BooleanField(default=False, verbose_name='Главное изображение')

    def __str__(self):
        return str(self.file)


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='cards')
    full_name = models.CharField(max_length=123, verbose_name='Имя владельца')
    number = models.CharField(max_length=123, verbose_name='Номер карты')
    cvv = models.CharField(max_length=123, verbose_name='CVV')
    expiry_date = models.DateField(verbose_name='Срок действия')

    def __str__(self):
        return self.full_name


class PaymentOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='payment_orders')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name='Карта', related_name='payment_orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='payment_orders')
    amount = models.PositiveIntegerField(verbose_name='Сумма')

    def __str__(self):
        return f'{self.user.username} - {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='favorites')

    def __str__(self):
        return f'{self.user.username} -> {self.product.title}'


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='feedbacks')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='feedbacks')
    rating = models.PositiveIntegerField(verbose_name='Оценка')
    comment = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.user.username} - {self.rating}★'


class FeedbackResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='responses')
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, verbose_name='Отзыв', related_name='responses')
    comment = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.user.username} - ответ на отзыв #{self.feedback.id}'
