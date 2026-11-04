from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import UserModel


class CategoryModel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"), db_index=True)
    image = models.ImageField(upload_to='category_images/', verbose_name=_("image"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class BrandModel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"), db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')


class ColorModel(models.Model):
    color = models.CharField(max_length=100, verbose_name=_("color"), db_index=True)

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = _('Color')
        verbose_name_plural = _('Colors')


class SizeModel(models.Model):
    size = models.CharField(max_length=100, verbose_name=_("size"), db_index=True)

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = _('Size')
        verbose_name_plural = _('Sizes')


class ProductModel(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("name"), db_index=True)
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_("category")
    )
    brand = models.ForeignKey(
        BrandModel,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_("brand")
    )
    colors = models.ManyToManyField(
        ColorModel,
        related_name='products',
        verbose_name=_("colors")
    )
    sizes = models.ManyToManyField(
        SizeModel,
        related_name='products',
        verbose_name=_("sizes")
    )
    image = models.ImageField(upload_to='product_images/', verbose_name=_("image"))
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name=_("price"))
    short_description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("short_description"))
    long_description = models.TextField(verbose_name=_("long_description"))
    discount = models.PositiveIntegerField(default=0, verbose_name=_("discount"))

    wishlist = models.ManyToManyField(
        UserModel,
        related_name='wishlist',
        blank=True,
        verbose_name=_("wishlist")
    )
    cart = models.ManyToManyField(
        UserModel,
        related_name='cart',
        blank=True,
        verbose_name=_("cart")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def get_price(self):
        if self.discount:
            return self.price - self.price / 100 * self.discount
        return self.price

    def is_discount(self):
        return True if self.discount else False
