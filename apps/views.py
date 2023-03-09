from django_filters import rest_framework as filters
from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView, \
    ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.models import Product, Category, Wishlist, User
from apps.serializers import ProductModelSerializer, WishListModelSerializer, CategoryModelSerializer, \
    CreateWishListModelSerializer


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    # parser_classes = (MultiPartParser,)
    # filterset_fields = ('category',)
    filterset_fields = ('name', 'price')


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
        serializer = WishListModelSerializer(request.user.wishlist)
        return Response(serializer.data)
