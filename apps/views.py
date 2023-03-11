from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.models import Product, Category, Wishlist, Basket
from apps.serializers import ProductModelSerializer, \
    WishListModelSerializer, CategoryModelSerializer, \
    BasketModelSerializer
from apps.shared.filters import ProductFilter
from apps.shared.permissions import IsAdminUser


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    parser_classes = (MultiPartParser,)
    filterset_class = ProductFilter
    permission_classes = (IsAdminUser,)


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = (IsAdminUser,)


class WishListAPIView(ModelViewSet):
    serializer_class = WishListModelSerializer
    queryset = Wishlist.objects.all()
    http_method_names = ('get', 'post', 'delete')
    lookup_field = 'product'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """**Delete user's wishlist**"""
        wishlist = request.user.wishlist_set.filter(product=kwargs.get('product'))
        if wishlist:
            wishlist.delete()
            return Response({'status': True, 'message': 'Product has been removed from wishlist'})
        return Response({'status': False, 'message': 'Product not found from your wishlist'},
                        status=status.HTTP_404_NOT_FOUND)


class BasketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketModelSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    lookup_field = 'product'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """***Delete product from user's basket**"""

        basket = request.user.basket_set.filter(product=kwargs.get('product'))
        if not basket:
            return Response({'status': False,
                             'message': 'Product not found from basket'},
                            status=status.HTTP_404_NOT_FOUND
                            )
        basket.delete()
        return Response({'status': True, 'message': 'Product has been removed from basket'})
