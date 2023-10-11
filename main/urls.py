from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import HomeView, AboutView, ContactView, ShoppingCartView, IncrementCountView, DecrementCountView, \
    JewelleryView, AddProductView, ProductAPIView, ProductDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('shopping/', ShoppingCartView.as_view(), name='shopping'),
    path('add-product/', AddProductView.as_view(), name='add-product'),
    path('jewellery/', JewelleryView.as_view(), name='jewellery'),
    path('product/', ProductAPIView.as_view(), name='product'),
    path('product-detail/', ProductDetailView.as_view(), name='product_detail'),
    path('increment-count', csrf_exempt(IncrementCountView.as_view()), name='increment'),
    path('decrement-count', csrf_exempt(DecrementCountView.as_view()), name='decrement'),
]
