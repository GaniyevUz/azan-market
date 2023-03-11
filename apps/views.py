from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, \
    get_object_or_404
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.models import Product, Category, Wishlist, Basket, User
from apps.serializers import ProductModelSerializer, \
    WishListModelSerializer, CategoryModelSerializer, \
    BasketModelSerializer
from apps.serializers.users import UserModelSerializer, UserAccountActivatonSerializer
from apps.shared.filters import ProductFilter
from apps.shared.permissions import IsAdminUser, IsAuthenticatedOrNewUSer
from apps.shared.verification import check


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


class UserModelViewSet(CreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    http_method_names = ('post', 'get', 'delete')
    permission_classes = (IsAuthenticatedOrNewUSer,)

    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'status': True, 'message': 'User has been created'})


class AccountActivateGenericAPIView(GenericAPIView):
    serializer_class = UserAccountActivatonSerializer
    http_method_names = ('post',)
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        code = request.data.get('code')
        if check(phone, code, True):
            user = get_object_or_404(User, phone=phone)
            user.is_active = True
            user.save()
            return Response({'status': True, 'message': 'Account has been activated'})
        raise ValidationError({'status': False, 'message': 'Invalid code'})
