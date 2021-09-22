from django.core.cache import cache

from core.models import Product, Order


def clear_cache():
    for key in cache.keys('*'):
        if 'products_frontend' in key:
            cache.delete(key)
    cache.delete('products_backend')


def product_created(data):
    clear_cache()

    Product.objects.create(
        id=data['id'],
        title=data['title'],
        description=data['description'],
        image=data['image'],
        price=data['price'],
    )


def product_updated(data):
    clear_cache()

    product = Product.objects.get(pk=data['id'])

    product.title = data['title']
    product.description = data['description']
    product.image = data['image']
    product.price = data['price']
    product.save()


def product_deleted(data):
    clear_cache()

    Product.objects.filter(pk=data).delete()


def order_created(data):
    order = Order()
    order.id = data['id']
    order.code = data['code']
    order.user_id = data['user_id']
    order.total = sum(item['ambassador_revenue'] for item in data['order_items'])
    order.save()
