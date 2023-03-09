from django.db.models import Model, CharField, DecimalField, ForeignKey, CASCADE, TextField, ImageField, \
    PositiveBigIntegerField

from apps.models.product_handout import BaseModel


class Product(BaseModel):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    description = TextField()
    category = ForeignKey('apps.Category', on_delete=CASCADE)
    quantity = PositiveBigIntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Category(BaseModel):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
