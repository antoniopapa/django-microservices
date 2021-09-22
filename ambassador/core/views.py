import json
import math
import random
import string
import time

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView

from app.producer import producer
from core.models import Product, Link, Order
from core.serializer import ProductSerializer, LinkSerializer
from core.services import UserService


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data
        data['is_ambassador'] = True
        return Response(UserService.post('register', data=data))


class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        data['scope'] = 'ambassador'

        res = UserService.post('login', data=data)

        response = Response()
        response.set_cookie(key='jwt', value=res['jwt'])
        response.data = {
            'message': 'success'
        }

        return response


class UserAPIView(APIView):
    def get(self, request):
        user = request.user_ms

        orders = Order.objects.filter(user_id=user['id'])
        user['revenue'] = sum(order.total for order in orders)

        return Response(user)


class LogoutAPIView(APIView):
    def post(self, request):
        UserService.post('logout', headers=request.headers)

        response = Response()
        response.delete_cookie(key='jwt')
        response.data = {
            'message': 'success'
        }
        return response


class ProfileInfoAPIView(APIView):
    def put(self, request, pk=None):
        return Response(UserService.put('users/info', data=request.data, headers=request.headers))


class ProfilePasswordAPIView(APIView):
    def put(self, request, pk=None):
        return Response(UserService.put('users/password', data=request.data, headers=request.headers))


class ProductFrontendAPIView(APIView):
    @method_decorator(cache_page(60 * 60 * 2, key_prefix='products_frontend'))
    def get(self, _):
        time.sleep(2)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductBackendAPIView(APIView):

    def get(self, request):
        products = cache.get('products_backend')
        if not products:
            time.sleep(2)
            products = list(Product.objects.all())
            cache.set('products_backend', products, timeout=60 * 30)  # 30 min

        s = request.query_params.get('s', '')
        if s:
            products = list([
                p for p in products
                if (s.lower() in p.title.lower()) or (s.lower() in p.description.lower())
            ])

        total = len(products)

        sort = request.query_params.get('sort', None)
        if sort == 'asc':
            products.sort(key=lambda p: p.price)
        elif sort == 'desc':
            products.sort(key=lambda p: p.price, reverse=True)

        per_page = 9
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * per_page
        end = page * per_page

        data = ProductSerializer(products[start:end], many=True).data
        return Response({
            'data': data,
            'meta': {
                'total': total,
                'page': page,
                'last_page': math.ceil(total / per_page)
            }
        })


class LinkAPIView(APIView):

    def post(self, request):
        user = request.user_ms

        serializer = LinkSerializer(data={
            'user_id': user['id'],
            'code': ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),
            'products': request.data['products']
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        json_data = json.dumps(serializer.data)
        producer.produce("admin_topic", key="link_created", value=json_data)
        producer.produce("checkout_topic", key="link_created", value=json_data)

        return Response(serializer.data)


class StatsAPIView(APIView):

    def get(self, request):
        user = request.user_ms

        links = Link.objects.filter(user_id=user['id'])

        return Response([self.format(link) for link in links])

    def format(self, link):
        orders = Order.objects.filter(code=link.code, complete=1)

        return {
            'code': link.code,
            'count': len(orders),
            'revenue': sum(o.ambassador_revenue for o in orders)
        }


class RankingsAPIView(APIView):
    def get(self, request):
        con = get_redis_connection("default")

        rankings = con.zrevrangebyscore('rankings', min=0, max=10000, withscores=True)

        return Response({
            r[0].decode("utf-8"): r[1] for r in rankings
        })
