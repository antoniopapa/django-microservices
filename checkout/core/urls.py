from django.urls import path
from .views import LinkAPIView, OrderAPIView, OrderConfirmAPIView

urlpatterns = [
    path('links/<str:code>', LinkAPIView.as_view()),
    path('orders', OrderAPIView.as_view()),
    path('orders/confirm', OrderConfirmAPIView.as_view()),
]
