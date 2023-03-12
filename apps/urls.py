from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import ProductModelViewSet, WishListAPIView, CategoryModelViewSet, BasketModelViewSet, UserModelViewSet

router = DefaultRouter()
router.register('products', ProductModelViewSet, basename='products')
router.register('category', CategoryModelViewSet, basename='category')
router.register('user/wishlist', WishListAPIView, basename='wishlist')
router.register('user/basket', BasketModelViewSet, basename='basket')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/account', UserModelViewSet.as_view(), name='account'),
]
