from modeltranslation.translator import TranslationOptions, translator

from .models import Product


class ProductTranslation(TranslationOptions):
    fields = ('title', 'description')


translator.register(Product, ProductTranslation)
