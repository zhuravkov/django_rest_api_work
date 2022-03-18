from rest_framework import serializers

from app_1.models import CustomUser, Order, WorkType


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'





class EachWorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()
    workType = EachWorkTypeSerializer(many=True)
    date = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'


    def get_date (self, obj):
        return obj.date.strftime("%d-%m-%Y, %H:%M:%S")

    def get_client (self, obj):
        return obj.client.email
