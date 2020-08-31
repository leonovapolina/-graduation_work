from django.db import models
from products.models import Product
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Payment(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'


class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)  # создание
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # обновление

    def __str__(self):
        return "Статус %s" % self.name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    client_name = models.CharField(max_length=64, blank=True, null=True, default=None)
    client_email = models.EmailField(blank=True, null=True, default=None)
    client_phone = models.CharField(max_length=48, blank=True, null=True, default=None)
    client_address = models.CharField(max_length=128, blank=True, null=True, default=None)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)  # создание заказа
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # обновление

    def __str__(self):
        return "Заказ %s %s" % (self.id, self.status.name)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, default=None)  # ссылка на таблицу заказ
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, default=None)
    number = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # price*number
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)  # создание заказа
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # обновление

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказа'

    def save(self, *args, **kwargs):
        price = self.product.price  # взяли цену из модели товара
        self.price = price  # добавили в нашу запись товаров заказа
        self.amount = int(self.number) * price  # считаем общую соимость товара

        super(ProductInOrder, self).save(*args, **kwargs)


def product_in_order_post_save(sender, instance, created, **kwags):
    order = instance.order  # взяли заказ
    products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)  # продукты заказа (активные)

    order_total_price = 0
    for item in products_in_order:
        order_total_price += item.amount  # считаем общую стоимость заказа

    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)  # сохраняем обновленные данные в заказе


post_save.connect(product_in_order_post_save, sender=ProductInOrder)  # вызов постсэйв сигнала


class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, default=None)
    nmb = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        price = self.product.price
        self.price = price
        self.amount = int(self.nmb) * price

        super(ProductInBasket, self).save(*args, **kwargs)
