from django.shortcuts import render

# Create your views here.
from app_1.models import CustomUser, Order
from app_1.serializers import UserSerializer, OrderSerializer


def index(request):

	return render(request, 'index.html')


# Create your views here.
from rest_framework import generics





class UsersApiView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class OrderApiView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()