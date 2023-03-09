from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import ProductModelViewSet, WishListAPIView, CategoryModelViewSet, BasketModelViewSet

router = DefaultRouter()
router.register('products', ProductModelViewSet, basename='products')
urlpatterns = [
    path('', include(router.urls)),
    path('category/', CategoryModelViewSet.as_view(), name='category'),
    path('user/wishlist/', WishListAPIView.as_view({'get': 'get', 'post': 'create'}), name='wishlist'),
    path('user/basket/', BasketModelViewSet.as_view({'get': 'get', 'post': 'create', 'patch': 'update'}), name='basket')
    # path('wishlist/add-product', WishListCreateAPIView.as_view(), name='wishlist'),

]
