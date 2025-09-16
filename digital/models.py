from itertools import product

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название категории')
    icon = models.ImageField(upload_to='icons/', verbose_name='Иконка', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, verbose_name='Слаг категории')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='subcategories', verbose_name='Родитель категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def get_icon(self):
        if self.icon:
            try:
                return self.icon.url
            except:
                return ''
        else:
            return ''

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание товара', null=True, blank=True)
    price = models.FloatField(verbose_name='Цена товара')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    color_name = models.CharField(max_length=50, verbose_name='Название цвета')
    color_code = models.CharField(max_length=10, verbose_name='Код цвета')
    discount = models.IntegerField(verbose_name='Скидка', null=True, blank=True)
    guarantee = models.IntegerField(null=True, blank=True, verbose_name='Гарантия')
    memory = models.IntegerField(null=True, blank=True, verbose_name='Память')
    width = models.CharField(max_length=50, verbose_name='Ширина', null=True, blank=True)
    depth = models.CharField(max_length=50, verbose_name='Глубина', null=True, blank=True)
    height = models.CharField(max_length=50, verbose_name='Высота', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, verbose_name='Слаг товара')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='products', verbose_name='Категория товара')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True, verbose_name='Брэнд')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    # def get_price(self):
    #     if self.discount:
    #         disc = (self.price * self.discount) / 100
    #         self.price -= disc
    #         return self.price
    #     else:
    #         return self.price

    # def get_price(self):
    #     if self.discount:
    #         discount_amount = (self.price * self.discount) / 100
    #         return self.price - discount_amount
    #     return self.price

    def get_price(self):
        if self.discount:
            disc = (self.price * self.discount) / 100
            new = self.price - disc
            return new
        else:
            return self.price

    def installment(self):
        total_with_markup = self.price * 1.4
        return round(total_with_markup / 12, 2)

    def get_memory(self):
        if 1 <= self.memory < 64:
            return f'{self.memory}TB'
        else:
            return f'{self.memory}GB'

    def get_guarantee_text(self):
        if self.guarantee is None:
            return "Нет"
        if self.guarantee == 1:
            return f"{self.guarantee} год"
        elif 2 <= self.guarantee <= 4:
            return f"{self.guarantee} года"
        else:
            return f"{self.guarantee} лет"

    def stock(self):
        if self.quantity >= 1:
            return f'{self.quantity} шт.'
        else:
            return f'Нет'

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return ''
        else:
            return ''


class GalleryProduct(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Фото товара')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images', verbose_name='Товар')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'


class Brand(models.Model):
    title = models.CharField(max_length=150, verbose_name='Бренд товара')
    slug = models.SlugField(unique=True, null=True, verbose_name='Слаг товара')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модель товара'
        verbose_name_plural = 'Бренды товаров'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')

    def __str__(self):
        return f'Профиль пользователя: {self.user.username}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f'{self.user.username}: {self.product.title}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные товары'


# =======================================================================================================================

class Order(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата начала заказа')
    is_completed = models.BooleanField(default=False, verbose_name='Статус заказа')
    payment = models.BooleanField(default=False, verbose_name='Статус платежа')
    shipping = models.BooleanField(default=True, verbose_name='Доставка')

    def __str__(self):
        return f'Заказ покупателя {self.customer.user.first_name} №: {self.pk}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    # Метод который будет возвращать сумму заказа
    # @property
    # def get_order_total_price(self):
    #     order_products = self.orderproduct_set.all()
    #     total_price = sum([i.get_total_price for i in order_products])
    #     return total_price

    @property
    def get_order_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([i.quantity * i.product.price for i in order_products])
        return total_price

    @property
    def get_order_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([i.quantity for i in order_products])
        return total_quantity


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(default=0, verbose_name='В количестве')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    @property
    def get_total_price(self):
        return self.quantity * self.product.get_price()


    def __str__(self):
        return f'Товар {self.product.title} для заказа №: {self.order.pk} '

    class Meta:
        verbose_name = 'Заказать товар'
        verbose_name_plural = 'Заказанные товары'


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    address = models.CharField(max_length=150, verbose_name='Адрес доставки (улица, дом, кв): ')
    phone = models.CharField(max_length=30, verbose_name='Номер телефона')
    comment = models.TextField(verbose_name='Комментарий к заказу', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата оформления доставки')
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name='Регион доставки')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город доставки')
    first_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Фамилия')
    email = models.EmailField(max_length=150, null=True, blank=True, verbose_name='Почта')

    def __str__(self):
        return f'Доставка для {self.customer.user.first_name}, заказ №: {self.order.pk}'

    class Meta:
        verbose_name = 'Доставку'
        verbose_name_plural = 'Адреса доставок'


class Region(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название области')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Область (Регион)'
        verbose_name_plural = 'Области (Регион)'


class City(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название области')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Область (Регион)', related_name='cities')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'