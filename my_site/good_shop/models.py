from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Product(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=50)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    # @property
    # def description_short(self) -> str:
    #     if len(self.description) < 30:
    #         return self.description
    #     return self.description[:20] + '...'

    def __str__(self) -> str:
        return f'Продукт: {self.name!r}'


class Order(models.Model):
    # class Meta:
    #     ordering = ['created_at']

    delivery_address = models.TextField(null=True, blank=True)
    promo = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='order')
