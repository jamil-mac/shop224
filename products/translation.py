from modeltranslation.translator import register, TranslationOptions

from products.models import CategoryModel, ColorModel, ProductModel


@register(CategoryModel)
class CategoryTranslationOptions(TranslationOptions):
    fields = 'name',


@register(ColorModel)
class ColorTranslationOptions(TranslationOptions):
    fields = 'color',


@register(ProductModel)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'short_description', 'long_description',)

