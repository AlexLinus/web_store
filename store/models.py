from django.db import models
from autoslug import AutoSlugField
from django.shortcuts import reverse

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False, verbose_name='Заголовок')
    slug = AutoSlugField(populate_from='title', verbose_name='название ссылки')
    price = models.DecimalField(max_digits=6, decimal_places=0, verbose_name='Цена')
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание товара')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    available = models.BooleanField(default=True, verbose_name='В наличии')
    is_active = models.BooleanField(default=False, verbose_name='Опубликовано')
    comments_open = models.BooleanField(default=True, verbose_name='Комментарии открыты')
    seo_title = models.CharField(max_length=220, blank=True, null=True)
    seo_description = models.TextField(max_length=220, blank=True, null=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.seo_title:
            self.seo_title = self.title
        if not self.seo_description:
            self.seo_description = self.description[:180]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('get_product_detail_url', kwargs={'category_slug': self.category.slug, 'product_slug': self.slug})

class Category(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False, verbose_name='Заголовок')
    slug = AutoSlugField(populate_from='title', verbose_name='Ссылка')
    description = models.TextField(verbose_name='Описание категории')
    seo_title = models.CharField(max_length=220, blank=True, null=True, verbose_name='SEO заголовок')
    seo_description = models.TextField(max_length=220, blank=True, null=True, verbose_name='SEO описание')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Опубликовано')

    class Meta:
        ordering = ['-title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.seo_title:
            self.seo_title = self.title

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('get_category_detail_url', kwargs={'category_slug': self.slug})

    def get_product_quantity(self):
        products = self.products.all()
        return len(products)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', default=None, blank=True, null=True, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='uploads/product_images/', default='default.jpg')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    is_main = models.BooleanField(default=False, verbose_name='Главное изображение')
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    class Meta:
        ordering = ['-product', '-pub_date']
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


from solo.models import SingletonModel

class SiteConfiguration(SingletonModel):
    main_telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона интернет магазина')
    main_adress = models.CharField(max_length=40, blank=True, null=True, verbose_name='Адрес интернет магазина')
    main_email = models.EmailField(default=None, blank=True, null=True, verbose_name='Электронная почта интернет магазина')
    main_seo_title = models.CharField(max_length=140, null=True, blank=True, verbose_name='SEO заголовок главной страницы')
    main_seo_description = models.TextField(max_length=200, null=True, blank=True, verbose_name='SEO описание главной страницы')
    top_selling_products = models.ManyToManyField('Product', verbose_name='Выберите самые продаваемые товары')
    menu_category_items = models.ManyToManyField('Category', default=None, blank=True, null=True, verbose_name='Категории включенные в меню')

    def __str__(self):
        return 'Основные настройки'

    class Meta:
        verbose_name='Настройки магазина'