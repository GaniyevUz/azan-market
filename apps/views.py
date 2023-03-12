from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg import openapi, utils
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.models import Product, Category, Wishlist, Basket, User
from apps.serializers import ProductModelSerializer, \
    WishListModelSerializer, CategoryModelSerializer, \
    BasketModelSerializer
from apps.serializers.users import UserModelSerializer
from apps.shared import permissions, filters as custom_filters


@method_decorator(name='create', decorator=utils.swagger_auto_schema(manual_parameters=[openapi.Parameter(
    name='images',
    in_=openapi.IN_FORM,
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_FILE),
    required=True,
    description='Product images'
)]))
class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    parser_classes = (MultiPartParser,)
    filterset_class = custom_filters.ProductFilter
    permission_classes = (permissions.IsAdminUser,)


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = (permissions.IsAdminUser,)


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


class UserModelViewSet(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    http_method_names = ('post', 'get', 'delete')
    permission_classes = (permissions.IsAuthenticatedOrNewUSer,)

    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'status': True, 'message': 'We have sent you a verification code to your phone number'})
