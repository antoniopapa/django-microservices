from django.core.management import BaseCommand
from core.models import Order, OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        orders = Order.objects.using('old').all()

        for order in orders:
            Order.objects.create(
                id=order.id,
                code=order.code,
                user_id=order.user_id,
                transaction_id=order.transaction_id,
                ambassador_email=order.ambassador_email,
                first_name=order.first_name,
                last_name=order.last_name,
                email=order.email,
                address=order.address,
                country=order.country,
                city=order.city,
                zip=order.zip,
                complete=order.complete
            )

        order_items = OrderItem.objects.using('old').all()

        for order_item in order_items:
            OrderItem.objects.create(
                id=order_item.id,
                order_id=order_item.order_id,
                product_title=order_item.product_title,
                price=order_item.price,
                quantity=order_item.quantity,
                admin_revenue=order_item.admin_revenue,
                ambassador_revenue=order_item.ambassador_revenue
            )
