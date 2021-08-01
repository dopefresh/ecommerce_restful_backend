from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    """
    Category of Product in ecommerce site
    """
    slug = models.SlugField()
    title = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'category'
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    """
    Subcategory of Product in ecommerce site
    """
    slug = models.SlugField()
    title = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'sub_category'
        verbose_name_plural = "sub_categories"

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Item(models.Model):
    """
    Product in ecommerce site
    """
    title = models.CharField(max_length=50, blank=False, null=False, unique=True)
    description = models.TextField()
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

    def __str__(self):
        return f'{self.title} {self.price}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class CartItem(models.Model):
    """
    User items in cart
    """
    quantity = models.IntegerField(default=1)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', related_name='cart_items', on_delete=models.CASCADE)

    class Meta:
        db_table = 'cart_item'
        verbose_name_plural = "cart_items"
        unique_together=('item', 'cart',)

    def __str__(self):
        return f"{self.item}: {self.quantity}"


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

    def __str__(self):
        return str(self.user)
