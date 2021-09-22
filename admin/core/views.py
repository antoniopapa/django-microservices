import json

from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from app.producer import producer
from .models import Product, Link, Order
from .serializers import ProductSerializer, LinkSerializer, OrderSerializer
from .services import UserService


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data
        data['is_ambassador'] = False

        return Response(UserService.post('register', data=data))


class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        data['scope'] = 'admin'

        res = UserService.post('login', data=data)

        response = Response()
        response.set_cookie(key='jwt', value=res['jwt'], httponly=True)
        response.data = {
            'message': 'success'
        }

        return response


class UserAPIView(APIView):
    def get(self, request):
        return Response(request.user_ms)


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


class AmbassadorAPIView(APIView):
    def get(self, _):
        users = UserService.get('users/')
        return Response(filter(lambda a: a['is_ambassador'] == 1, users))


class ProductGenericAPIView(
    generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)

        return self.list(request)

    def post(self, request):
        response = self.create(request)
        json_data = json.dumps(response.data)
        producer.produce('ambassador_topic', key='product_created', value=json_data)
        producer.produce('checkout_topic', key='product_created', value=json_data)
        return response

    def put(self, request, pk=None):
        response = self.partial_update(request, pk)
        json_data = json.dumps(response.data)
        producer.produce('ambassador_topic', key='product_updated', value=json_data)
        producer.produce('checkout_topic', key='product_updated', value=json_data)
        return response

    def delete(self, request, pk=None):
        response = self.destroy(request, pk)
        json_data = json.dumps(pk)
        producer.produce('ambassador_topic', key='product_deleted', value=json_data)
        producer.produce('checkout_topic', key='product_deleted', value=json_data)
        return response


class LinkAPIView(APIView):
    def get(self, request, pk=None):
        links = Link.objects.filter(user_id=pk)
        serializer = LinkSerializer(links, many=True)
        return Response(serializer.data)


class OrderAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
