"""
Definition of models.
"""

from django.db import models
from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from tabnanny import verbose
from django.contrib.auth.models import User


class Blog(models.Model):
    title = models.CharField(max_length=100, unique_for_date="posted", verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")
    image = models.FileField(default='temp.jpg', verbose_name="Путь к картинке")

    # Методы класса:
    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self):
        return self.title

    # Метаданные:
    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "Cтатья блога"
        verbose_name_plural = "Cтатьи блога"


admin.site.register(Blog)


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментарий")
    date = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Дата комментария")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Авторк Комментария")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья комментария")

    # Методы класса:
    def __str__(self):
        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post)

    # Метаданные:
    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарий к статье блога"
        verbose_name_plural = "Комментарии к статье блога"


admin.site.register(Comment)


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "Categories"
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

admin.site.register(Category)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(default='temp.jpg', verbose_name="Путь к картинке")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "Products"
        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

admin.site.register(Product)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "Carts"
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

admin.site.register(Cart)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "CartItems"
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"

admin.site.register(CartItem)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    statuses = (
        ('new', 'Новый'),
        ('in_progress', 'В обработке'),
        ('confirmed', 'Подтвержден'),
        ('sent', 'Отправлен'),
        ('done', 'Завершен'),
        ('canceled', 'Отменен'),
    )
    status = models.CharField(max_length=20, choices=statuses, default='new')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Orders"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

admin.site.register(Order)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "OrderItems"
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

admin.site.register(OrderItem)


class Feedback(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=255,
        choices=(
            ('male', 'Мужской'),
            ('female', 'Женский')
        )
    )
    internet = models.CharField(
        max_length=255,
        choices=(
            ('1', 'Каждый день'),
            ('2', 'Несколько раз в день'),
            ('3', 'Несколько раз в неделю'),
            ('4', 'Несколько раз в месяц')
        )
    )
    notice = models.BooleanField()
    email = models.EmailField()
    message = models.TextField()

    class Meta:
        db_table = "Feedbacks"
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

admin.site.register(Feedback)
