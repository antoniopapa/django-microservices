from django.urls import path, include

from .views import (
    AmbassadorAPIView, ProductGenericAPIView, LinkAPIView, OrderAPIView, RegisterAPIView,
    LoginAPIView, UserAPIView, LogoutAPIView, ProfileInfoAPIView, ProfilePasswordAPIView
)

urlpatterns = [
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('user', UserAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('users/info', ProfileInfoAPIView.as_view()),
    path('users/password', ProfilePasswordAPIView.as_view()),
    path('ambassadors', AmbassadorAPIView.as_view()),
    path('products', ProductGenericAPIView.as_view()),
    path('products/<str:pk>', ProductGenericAPIView.as_view()),
    path('users/<str:pk>/links', LinkAPIView.as_view()),
    path('orders', OrderAPIView.as_view()),
]
