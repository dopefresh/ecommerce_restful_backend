from django.db import models
from django.conf import settings
from django.utils.text import slugify

from PIL import Image


def company_logo_directory(instance, filename):
    return f'{instance.name}/logos/{filename}'


def company_product_directory(instance, filename):
    return f'{instance.company.name}/products/{filename}'


class Company(models.Model):
    name = models.CharField(max_length=500, unique=True)
    location = models.CharField(max_length=500)
    phone_number = models.CharField(
        max_length=30, 
        blank=False, null=False
    )
    logo = models.ImageField(
        upload_to=company_logo_directory,
        blank=True, null=True
    )
    slug = models.SlugField(blank=True)
    
    class Meta:
        db_table = 'company'
        verbose_name_plural = "Компании"

    def __str__(self):
        return f'Company name: {self.name}\n{self.phone_number}\n{self.location}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
        imag = Image.open(self.logo.path)
        if imag.width > 400 or imag.height> 300:
            output_size = (400, 300)
            imag.thumbnail(output_size)
            imag.save(self.logo.path)


class Category(models.Model):
    """
    Category of Product in ecommerce site
    """
    slug = models.SlugField(blank=True)
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'category'
        verbose_name_plural = "Категории товаров"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    """
    Subcategory of Product in ecommerce site
    """
    slug = models.SlugField(blank=True)
    title = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(
        'Category', 
        on_delete=models.CASCADE,
        related_name='sub_categories'
    )
    
    class Meta:
        db_table = 'sub_category'
        verbose_name_plural = "Подкатегории товаров"

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Item(models.Model):
    """
    Product in ecommerce site
    """
    title = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=False, null=False)
    product_image = models.ImageField(
        upload_to=company_product_directory,
        blank=True, null=True
    )
    
    slug = models.SlugField(blank=True)
    sub_category = models.ForeignKey(
        'SubCategory', 
        on_delete=models.SET_NULL,
        null=True,
        related_name='items'
    )
    company = models.ForeignKey(
        'Company',
        on_delete=models.SET_NULL,
        null=True
    )
    
    class Meta:
        db_table = 'item'
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f'{self.title} {self.price}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
        imag = Image.open(self.product_image.path)
        if imag.width > 400 or imag.height> 300:
            output_size = (400, 300)
            imag.thumbnail(output_size)
            imag.save(self.product_image.path)


class OrderItem(models.Model):
    """
    User items in his order
    """
    quantity = models.IntegerField(default=1)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', related_name='order_items', on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_item'
        verbose_name_plural = "Добавленные в корзину пользователем продукты"
        unique_together=('item', 'order',)

    def __str__(self):
        return f"{self.item}: {self.quantity}"


class Order(models.Model):
    """
    User's order object
    """
    ordered = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(
        blank=True, null=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    
    class Meta:
        db_table = 'order'
        verbose_name_plural = "Корзина пользователя"

    def __str__(self):
        return str(self.user)


class Step(models.Model):
    """
    Steps, that's order is taking before getting to user

    1. Payment
    2. Packaging
    3. Transportation
    4. Delivery in user's city
    """
    
    name_step = models.CharField(
        max_length=50, 
        default='Оплата'
    )
    orders = models.ManyToManyField(
        Order,
        related_name='steps',
        through='OrderStep'
    )


class OrderStep(models.Model):
    step = models.ForeignKey(
        'Step',
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE
    )
    date_step_begin = models.DateField(null=True)
    date_step_end = models.DateField(null=True)

