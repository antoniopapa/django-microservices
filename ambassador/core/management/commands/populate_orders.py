from django.core.management import BaseCommand
from django.db import connections

from core.models import Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        with connections['old'].cursor() as cursor:
            cursor.execute("SELECT * FROM core_order WHERE complete = 1")
            orders = cursor.fetchall()

            for order in orders:
                cursor.execute("SELECT * FROM core_orderitem WHERE order_id = '" + str(order[0]) + "'")
                order_items = cursor.fetchall()

                Order.objects.create(
                    id=order[0],
                    code=order[2],
                    user_id=order[14],
                    total=sum(item[5] for item in order_items)
                )
