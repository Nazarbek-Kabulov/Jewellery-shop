from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.FloatField()
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def create(self, validated_data):
        return super().save(**validated_data)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class Picture(models.Model):
    image = models.ImageField(upload_to='pics')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Picture')
        verbose_name_plural = _('Pictures')


class Shopping_cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = _('Shopping_cart')
        verbose_name_plural = _('Shopping_carts')


class Comment(models.Model):
    name = models.CharField(max_length=20, verbose_name=_('name'))
    email = models.EmailField(verbose_name=_('email'))
    phone = models.CharField(max_length=13, verbose_name=_('phone'))
    message = models.TextField(max_length=500, verbose_name=_('message'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
