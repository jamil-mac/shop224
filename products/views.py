from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from blog.models import BannerModel
from products.models import ProductModel, CategoryModel, BrandModel, ColorModel, SizeModel


class HomeListView(ListView):
    template_name = 'index.html'
    queryset = ProductModel.objects.order_by('-pk')[:3]
    context_object_name = 'products'

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryModel.objects.order_by('-pk')[:3]
        context['banner'] = BannerModel.objects.last()

        return context


class ShopListView(ListView):
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        qs = ProductModel.objects.order_by('-pk')

        q = self.request.GET.get('q')
        category = self.request.GET.get('category')
        brand = self.request.GET.get('brand')
        color = self.request.GET.get('color')
        size = self.request.GET.get('size')

        if q:
            qs = qs.filter(name__icontains=q)

        if category:
            qs = qs.filter(category_id=category)

        if brand:
            qs = qs.filter(brand_id=brand)

        if color:
            qs = qs.filter(color_id=color)

        if size:
            qs = qs.filter(size_id=size)

        return qs

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryModel.objects.order_by('-pk')
        context['brands'] = BrandModel.objects.order_by('-pk')
        context['colors'] = ColorModel.objects.order_by('-pk')
        context['sizes'] = SizeModel.objects.order_by('-pk')

        return context


class ProductDetailView(DetailView):
    template_name = 'shop-single.html'
    model = ProductModel
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = self.get_object().category.products.order_by('-pk').exclude(
            pk=self.get_object().pk)[:10]

        return context


@login_required
def wishlist_create(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)
    user = request.user

    if user in product.wishlist.all():
        product.wishlist.remove(user)
    else:
        product.wishlist.add(user)

    return redirect(request.GET.get('next', '/'))


@login_required
def wishlist_list(request):
    products = request.user.wishlist.order_by('-pk')

    context = {
        'products': products
    }

    return render(request, 'wishlist.html', context)


@login_required
def wishlist_delete(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)
    user = request.user

    if user in product.wishlist.all():
        product.wishlist.remove(user)

    return redirect(request.GET.get('next', '/'))


@login_required
def cart_create(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)
    user = request.user

    if user in product.cart.all():
        product.cart.remove(user)
    else:
        product.cart.add(user)

    return redirect(request.GET.get('next', '/'))


@login_required
def cart_list(request):
    products = request.user.cart.order_by('-pk')
    related = ProductModel.objects.all()[:10]

    context = {
        'products': products,
        'related': related
    }

    return render(request, 'cart.html', context)


@login_required
def cart_delete(request, pk):
    product = get_object_or_404(ProductModel, pk=pk)
    user = request.user

    if user in product.cart.all():
        product.cart.remove(user)

    return redirect(request.GET.get('next', '/'))
