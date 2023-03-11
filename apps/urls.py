from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import ProductModelViewSet, WishListAPIView, CategoryModelViewSet, BasketModelViewSet, UserModelViewSet, \
    AccountActivateGenericAPIView

router = DefaultRouter()
router.register('products', ProductModelViewSet, basename='products')
router.register('category', CategoryModelViewSet, basename='category')
# router.register('user/account', UserModelViewSet, basename='account')
router.register('user/wishlist', WishListAPIView, basename='wishlist')
router.register('user/basket', BasketModelViewSet, basename='basket')

urlpatterns = [
    path('', include(router.urls)),
    path('user/account', UserModelViewSet.as_view(), name='account'),
    path('user/account/activate', AccountActivateGenericAPIView.as_view(), name='account-activate'),
]
