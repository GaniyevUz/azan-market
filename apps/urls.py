from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import ProductModelViewSet, WishListAPIView, CategoryModelViewSet

router = DefaultRouter()
router.register('products', ProductModelViewSet, basename='products')
urlpatterns = [
    path('products/', include(router.urls)),
    path('category/', CategoryModelViewSet.as_view(), name='category'),
    path('wishlist/', WishListAPIView.as_view({'get': 'get', 'post': 'create'}), name='wishlist'),
]
