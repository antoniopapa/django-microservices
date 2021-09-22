from rest_framework import serializers

from core.models import Product, Link


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductRelatedField(serializers.StringRelatedField):
    def to_representation(self, value):
        return ProductSerializer(value).data

    def to_internal_value(self, data):
        return data


class LinkSerializer(serializers.ModelSerializer):
    products = ProductRelatedField(many=True)

    class Meta:
        model = Link
        fields = '__all__'
