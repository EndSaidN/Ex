from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=80)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    price = models.IntegerField(default=0)
    picture = models.ImageField('uploads/products')

    @staticmethod
    def get_product_by_id(product_id):
        return Product.objects.filter(id__in=product_id)

    @staticmethod
    def get_all_products():
        return Product.objects.all()
