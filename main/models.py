from django.db import models



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
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    user = models.ForeignKey('user.MyUser', on_delete=models.CASCADE, verbose_name='Пользователь', related_name='products')
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


class Favorite(models.Model):
    user = models.ForeignKey('user.MyUser', on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')

    def __str__(self):
        return f"{self.user} - {self.product}"






