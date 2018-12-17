from django.db import models
from store.models import Product

# Create your models here.
class Order(models.Model):
    class Meta:
        ordering = ['-create_date']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    first_name = models.CharField(max_length=20, blank=False, null=False, verbose_name='Имя')
    last_name = models.CharField(max_length=25, blank=False, null=False, verbose_name='Фамилия')
    phone = models.CharField(max_length=18, blank=False, null=False, verbose_name='Ваш номер телефона')
    email = models.EmailField(blank=True, null=True, verbose_name='Ваш e-mail')
    city = models.CharField(max_length=25, blank=True, null=True, verbose_name='Город доставки')
    address = models.CharField(max_length=50, blank=True, null=True, verbose_name='Адрес доставки')
    notes = models.TextField(verbose_name='Пожелания')
    create_date = models.DateTimeField(auto_now_add=True)
    total_price = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Итоговая сумма заказа')

    def __str__(self):
        return 'Заказ от {} из города {}'.format(self.first_name, self.city)

    def get_total_price(self):
        total = 0
        for item in self.items.all():
            total += (item.price*item.quantity)
        return total

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.get_total_price()
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары в заказе'

    order = models.ForeignKey('Order', related_name='items', verbose_name='Заказ', null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_item', verbose_name='Товар', null=True, on_delete=models.CASCADE)
    price = models.DecimalField(blank=True, null=True, max_digits=6, default=0, decimal_places=0, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return str(self.id) + ' - ' + self.product.title

    def get_cost(self):
        return self.price*self.quantity

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    items = models.ManyToManyField(OrderItem, verbose_name='cart_items')
    cart_total = models.DecimalField(default=0, decimal_places=0, max_digits=7, verbose_name='Итоговая сумма')

    def __str__(self):
        return 'Идентификатор корзины #{}'.format(self.id)