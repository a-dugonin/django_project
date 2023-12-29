from django.core.management import BaseCommand
from good_shop.models import Product


class Command(BaseCommand):
    """
    Creates product
    """

    def handle(self, *args, **options):
        self.stdout.write('Создайте продукт')
        products_name = [
            'Яблоки',
            'Апельсины',
            'Бананы'
        ]
        for product_name in products_name:
            product, create = Product.objects.get_or_create(name=product_name)
            self.stdout.write(f'Создан продукт {product_name}')

        self.stdout.write(self.style.SUCCESS('Продукт создан'))
