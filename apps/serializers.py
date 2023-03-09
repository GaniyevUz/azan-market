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
        wishlist = {'products': list(instance.product.values('id', 'name', 'price', 'category', 'description'))}
        return wishlist


class CreateWishListModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    product = IntegerField()

    class Meta:
        model = Wishlist
        fields = ('id', 'product', 'user')

    def create(self, validated_data):
        # user = User.objects.get(id=validated_data['user'].id)
        user = validated_data['user']
        user.wishlist.product.add(validated_data['product'])
        user.save()
        return user.wishlist

    def to_representation(self, instance):
        return {'status': 'product has been added to wishlist'}


class BasketModelSerializer(ModelSerializer):
    class Meta:
        model = Basket
        fields = ('id', 'product', 'user', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
