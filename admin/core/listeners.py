from .models import Order, OrderItem
from .serializers import LinkSerializer


def link_created(data):
    print(data)

    serializer = LinkSerializer(data={
        'id': data['id'],
        'user_id': data['user_id'],
        'code': data['code'],
        'products': list(p['id'] for p in data['products'])
    })
    serializer.is_valid(raise_exception=True)
    serializer.save()


def order_created(data):
    order = Order()
    order.id = data['id']
    order.transaction_id = data['transaction_id']
    order.code = data['code']
    order.user_id = data['user_id']
    order.ambassador_email = data['email']
    order.first_name = data['first_name']
    order.last_name = data['last_name']
    order.email = data['email']
    order.address = data['address']
    order.country = data['country']
    order.city = data['city']
    order.zip = data['zip']
    order.save()

    for item in data['order_items']:
        order_item = OrderItem()
        order_item.id = item['id']
        order_item.order = order
        order_item.product_title = item['product_title']
        order_item.price = item['price']
        order_item.quantity = item['quantity']
        order_item.ambassador_revenue = item['ambassador_revenue']
        order_item.admin_revenue = item['admin_revenue']
        order_item.save()
