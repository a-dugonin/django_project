from django.core.management import BaseCommand

from good_shop.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        order = Order.objects.first()
        if not order:
            self.stdout.write('Заказ не найден')
            return
        product = Product.objects.all()

        for product in product:
            order.products.add(product)

        order.save()
        self.stdout.write(
            self.style.SUCCESS(f'Продукты {order.products.all()} добавлены в заказ {order}')
        )