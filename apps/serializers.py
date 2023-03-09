from django.db.models import QuerySet
from rest_framework.fields import CurrentUserDefault, HiddenField, IntegerField
from rest_framework.serializers import ModelSerializer

from apps.models import Product, Wishlist, Category, User, Basket


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'category', 'description', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class WishListModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Wishlist
        fields = ('id', 'product', 'user', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def to_representation(self, instance):
        wishlist = {'status': False, 'message': 'Your basket is empty'}
        if hasattr(instance, 'product'):
            wishlist = {'products': list(instance.product.values('id', 'name', 'price', 'category', 'description'))}
        return wishlist


class CreateWishListModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    product = IntegerField()

    class Meta:
        model = Wishlist
        fields = ('id', 'product', 'user')

    def create(self, validated_data):
        product = Product.objects.filter(id=validated_data['product']).first()
        if product:
            user = validated_data['user']
            wishlist, _ = Wishlist.objects.get_or_create(user=user)
            wishlist.product.add(product)
            return wishlist
        return {'status': False, 'message': 'product not found'}

    def to_representation(self, instance):
        if isinstance(instance, Wishlist):
            return {'status': True, 'message': 'product has been added to wishlist'}
        return instance


class BasketModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Basket
        fields = ('id', 'product', 'user', 'quantity', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def to_representation(self, instance):
        basket = {'status': False, 'message': 'Your basket is empty'}
        if hasattr(instance, 'product'):
            basket = {'products': list(instance.product.values('id', 'name', 'price', 'category', 'description'))}
        return basket


class CreateBasketModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    product = IntegerField()

    class Meta:
        model = Basket
        fields = ('id', 'product', 'user', 'quantity', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        user = validated_data['user']
        user.basket.product.add(validated_data['product'])
        user.save()
        return user.basket

    def to_representation(self, instance):
        return {'status': True, 'message': 'product has been added to your basket'}
