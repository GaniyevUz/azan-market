from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView, \
    ListCreateAPIView, GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.models import Product, Category, Wishlist, User, Basket
from apps.serializers import ProductModelSerializer, WishListModelSerializer, CategoryModelSerializer, \
    CreateWishListModelSerializer, BasketModelSerializer, CreateBasketModelSerializer
from apps.shared.filters import ProductFilter


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    # parser_classes = (MultiPartParser,)
    # filterset_fields = ('category',)
    filterset_class = ProductFilter
    # filterset_fields = ('name', 'price')


class CategoryModelViewSet(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


class WishListAPIView(ModelViewSet):
    serializer_class = WishListModelSerializer
    queryset = Wishlist.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateWishListModelSerializer
        return super().get_serializer_class()

    def get(self, request, *args, **kwargs):
        """**Get user's wishlist**"""

        try:
            serializer = WishListModelSerializer(request.user.wishlist)
            return Response(serializer.data)
        except User.wishlist.RelatedObjectDoesNotExist:  # noqa
            return Response({'status': False, 'message': 'User has no wishlist'}, status=status.HTTP_404_NOT_FOUND)


# class WishListCreateAPIView(GenericAPIView):
#     serializer_class = CreateWishListModelSerializer
#     queryset = Wishlist.objects.all()
#
#     def get_queryset(self):
#         return super().get_queryset().filter(user=self.request.user)
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(request)
#         return Response(serializer.data)

class BasketModelViewSet(ModelViewSet):
    serializer_class = BasketModelSerializer
    queryset = Basket.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateBasketModelSerializer
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        basket = request.user.basket
        return Response()

    def get(self, request, *args, **kwargs):
        """**Get user's basket**"""
        basket = getattr(request.user, 'basket', {})
        serializer = self.serializer_class(basket)
        return Response(serializer.data)
