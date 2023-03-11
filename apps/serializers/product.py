from rest_framework.fields import CurrentUserDefault, HiddenField, IntegerField
from rest_framework.serializers import ModelSerializer

from apps.models import Product, Wishlist, Category, Basket, ProductImage


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class ProductModelSerializer(ModelSerializer):
    # images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'description', 'price', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    # def create(self, validated_data):
    #     images_data = validated_data.pop('images', [])
    #     product = Product.objects.create(**validated_data)
    #     for image_data in images_data:
    #         ProductImage.objects.create(product=product, **image_data)
    #     return product
    #
    # def update(self, instance, validated_data):
    #     images_data = validated_data.pop('images', [])
    #     instance = super().update(instance, validated_data)
    #     instance.images.all().delete()
    #     for image_data in images_data:
    #         ProductImage.objects.create(product=instance, **image_data)
    #     return instance


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class WishListModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    product = IntegerField()

    class Meta:
        model = Wishlist
        fields = ('id', 'product', 'user', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        product = Product.objects.filter(id=validated_data['product']).first()
        if product:
            user = validated_data['user']
            wishlist, _ = Wishlist.objects.get_or_create(user=user, product=product)
            return {'status': True, 'message': 'product has been added to wishlist'}
        return {'status': False, 'message': 'product not found'}

    def to_representation(self, instance):
        wishlist = {'status': False, 'message': 'Your basket is empty'}
        if hasattr(instance, 'product'):
            wishlist = ProductModelSerializer(instance.product).data
        return wishlist


class BasketModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    # product = IntegerField()

    class Meta:
        model = Basket
        fields = ('id', 'product', 'user', 'quantity', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        product = Product.objects.filter(id=validated_data['product']).first()
        if product:
            user = validated_data['user']
            basket, _ = Basket.objects.get_or_create(user=user, product=product)
            return basket
        return {'status': False, 'message': 'product not found'}

    def to_representation(self, instance):
        basket = {'status': False, 'message': 'Your basket is empty'}
        if isinstance(instance, Basket):
            basket = ProductModelSerializer(instance.product).data
        return basket
