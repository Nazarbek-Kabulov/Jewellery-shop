from modeltranslation.admin import TranslationAdmin
from django.contrib import admin
from .models import Product, Shopping_cart, Picture, Comment


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    pass


admin.site.register((Shopping_cart, Picture, Comment))
