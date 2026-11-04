from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from products.models import CategoryModel, BrandModel, ColorModel, SizeModel, ProductModel


class MyTranslationAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(CategoryModel)
class CategoryModelAdmin(MyTranslationAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(BrandModel)
class BrandModelAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(ColorModel)
class ColorModelAdmin(MyTranslationAdmin):
    list_display = ['color']
    search_fields = ['color']
    list_filter = ['color']


@admin.register(SizeModel)
class SizeModelAdmin(admin.ModelAdmin):
    list_display = ['size']
    search_fields = ['size']
    list_filter = ['size']


@admin.register(ProductModel)
class ProductModelAdmin(MyTranslationAdmin):
    list_display = ['name', 'category', 'brand', 'get_price']
    search_fields = ['name']
    list_filter = ['name', 'brand', 'category']
    readonly_fields = ['get_price']
