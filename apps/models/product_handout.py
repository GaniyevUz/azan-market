from django.db.models import Model, ForeignKey, CASCADE, ImageField, PositiveIntegerField, DateTimeField, OneToOneField, \
    ManyToManyField


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


#
class ProductImage(BaseModel):
    product = ForeignKey('apps.Product', CASCADE)
    image = ImageField(upload_to='products/')

    def __str__(self):
        return self.product.name

    class Meta:
        db_table = 'product_images'
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'


class Basket(BaseModel):
    user = ForeignKey('apps.User', CASCADE)
    product = ForeignKey('apps.Product', CASCADE)
    quantity = PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user} {self.product.name} - {self.quantity}"

    class Meta:
        db_table = 'baskets'
        verbose_name = 'Basket'
        verbose_name_plural = 'Baskets'


class Wishlist(BaseModel):
    # user = OneToOneField('apps.User', CASCADE)
    # product = ManyToManyField('apps.Product', related_name='products')
    user = ForeignKey('apps.User', CASCADE)
    product = ForeignKey('apps.Product', CASCADE)

    def __str__(self):
        return self.user_set.first().phone

    class Meta:
        db_table = 'wishlists'
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'
