from django.contrib.auth.models import User
from django.core.management import BaseCommand
from good_shop.models import Order


class Command(BaseCommand):
    """
    Creates order
    """

    def handle(self, *args, **options):
        self.stdout.write('Создайте заказ')
        user = User.objects.get(username='admin')
        order = Order.objects.get_or_create(
            delivery_address='ул. Каляева 263/4',
            promo='new_year10',
            user=user
        )

        self.stdout.write(f'Заказ создан {order}')
