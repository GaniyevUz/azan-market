from django.db.models import Model, ForeignKey, CASCADE, ImageField, PositiveIntegerField, DateTimeField, OneToOneField, \
    ManyToManyField


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProductImage(BaseModel):
    product = ForeignKey('apps.Product', on_delete=CASCADE)
    image = ImageField(upload_to='products/')

    def __str__(self):
        return self.product.name

    class Meta:
        db_table = 'product_images'
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'


class Basket(BaseModel):
    user = OneToOneField('apps.User', on_delete=CASCADE)
    product = ForeignKey('apps.Product', on_delete=CASCADE)
    quantity = PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

    class Meta:
        db_table = 'baskets'
        verbose_name = 'Basket'
        verbose_name_plural = 'Baskets'


class Wishlist(BaseModel):
    user = OneToOneField('apps.User', on_delete=CASCADE)
    product = ManyToManyField('apps.Product', related_name='products')

    def __str__(self):
        return self.product.first().name

    class Meta:
        db_table = 'wishlists'
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'
