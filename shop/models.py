from django.db import models
from django.conf import settings


class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=30)

    class Meta:
        db_table = 'category'
        verbose_name_plural = "categories"


class SubCategory(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=30)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'sub_category'
        verbose_name_plural = "sub_categories"


class Item(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=1000)
    price = models.IntegerField(blank=False, null=False)
    
    slug = models.SlugField()
    sub_category = models.ForeignKey(
        'SubCategory', 
        on_delete=models.SET_NULL,
        null=True
    )
    
    class Meta:
        db_table = 'item'
        verbose_name_plural = "items"


class CartItem(models.Model):
    quantity = models.IntegerField(default=1)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)

    class Meta:
        db_table = 'cart_item'
        verbose_name_plural = "cart_items"


class Cart(models.Model):
    ordered = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(
        blank=True, null=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    
    class Meta:
        db_table = 'cart'
        verbose_name_plural = "carts"



