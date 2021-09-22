from core.models import Product
from core.serializers import LinkSerializer


def product_created(data):
    Product.objects.create(
        id=data['id'],
        title=data['title'],
        description=data['description'],
        image=data['image'],
        price=data['price'],
    )


def product_updated(data):
    product = Product.objects.get(pk=data['id'])

    product.title = data['title']
    product.description = data['description']
    product.image = data['image']
    product.price = data['price']
    product.save()


def product_deleted(data):
    Product.objects.filter(pk=data).delete()


def link_created(data):
    print(data)
    serializer = LinkSerializer(data={
        'id': data['id'],
        'user_id': data['user_id'],
        'code': data['code'],
        'products': data['products']
    })
    serializer.is_valid(raise_exception=True)
    serializer.save()
