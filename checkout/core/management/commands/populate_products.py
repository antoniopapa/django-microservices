from django.core.management import BaseCommand
from core.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.using('old').all()

        for product in products:
            Product.objects.create(
                id=product.id,
                title=product.title,
                description=product.description,
                image=product.image,
                price=product.price
            )
