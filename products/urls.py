from django.urls import path

from products import views

app_name = 'products'

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('shop/', views.ShopListView.as_view(), name='shop'),
    path('detail/<int:pk>/', views.ProductDetailView.as_view(), name='detail'),

    path('wishlist/<int:pk>/', views.wishlist_create, name='wishlist-create'),
    path('wishlist/', views.wishlist_list, name='wishlist-list'),
    path('wishlist/<int:pk>/delete/', views.wishlist_delete, name='wishlist-delete'),

    path('cart/<int:pk>/', views.cart_create, name='cart-create'),
    path('cart/', views.cart_list, name='cart-list'),
    path('cart/<int:pk>/delete/', views.cart_delete, name='cart-delete'),
]
