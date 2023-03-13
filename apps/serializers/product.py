from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault, HiddenField, IntegerField
from rest_framework.serializers import ModelSerializer

from apps.models import Product, Wishlist, Category, Basket, ProductImage


class CreateProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'product')


class ProductModelSerializer(ModelSerializer):
    images = serializers.ListField(write_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'description', 'images', 'price', 'quantity', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
        for image_data in images_data:
            ser = CreateProductImageSerializer(data={'image': image_data, 'product': product.id})
            ser.is_valid(raise_exception=True)
            ser.save()
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        instance = super().update(instance, validated_data)
        instance.images.all().delete()
        for image_data in images_data:
            image = CreateProductImageSerializer(data={'image': image_data, 'product': instance.id})
            image.is_valid(raise_exception=True)
            image.save()
        return instance

    def to_representation(self, instance):
        product = super().to_representation(instance)
        product['images'] = [i.image.url for i in instance.productimage_set.all()]
        product.move_to_end('created_at')
        product.move_to_end('updated_at')
        return product

    @property
    def data(self):
        return self.to_representation(self.instance)


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

    @property
    def data(self):
        return self.to_representation(self.instance)


class BasketModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Basket
        fields = ('id', 'product', 'user', 'quantity', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        product = validated_data.get('product')
        if not isinstance(product, Product):
            product = Product.objects.filter(id=product).first()
        if product:
            if getattr(product, 'quantity') < validated_data['quantity'] or product.quantity < 1:
                raise ValidationError({'status': False, 'message': 'This product is out of stock for this quantity'})
            user = validated_data['user']
            basket, _ = Basket.objects.get_or_create(user=user, product=product)
            return basket
        raise ValidationError({'status': False, 'message': 'product not found'})

    def to_representation(self, instance):
        basket = ProductModelSerializer(instance.product).data
        return basket


class UpdateBasketModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    quantity = IntegerField(min_value=1)

    class Meta:
        model = Basket
        fields = ('id', 'user', 'quantity')

    def update(self, instance, validated_data):
        quantity = validated_data.get('quantity')
        if not isinstance(instance, Basket):
            instance = Basket.objects.filter(id=instance).first()
        if instance.product.quantity < quantity or quantity < 1:
            raise ValidationError({'status': False, 'message': 'This product is out of stock for this quantity'})
        instance.quantity = quantity
        instance.save()
        return instance

    # @property
    # def data(self):
    #     return BasketModelSerializer(self.instance).data
