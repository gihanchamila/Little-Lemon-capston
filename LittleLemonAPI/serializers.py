from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User

"""
    Serializers are used to convert complex data types, like querysets and model instances, into native Python datatypes.
    They also handle deserialization, allowing parsed data to be converted back into complex types.
    Serializers are similar to Django Forms, but they are not tied to any specific view or template.

    Serializers can be used to validate data, and they can also be used to create or update model instances.
    Serializers can be used to create custom fields, and they can also be used to create custom validation methods.
    
"""

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    # category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'category', 'featured']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )


    def validate(self, attrs):
        attrs['price'] = attrs['quantity'] * attrs['unit_price']
        return attrs

    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'unit_price', 'quantity', 'price']
        extra_kwargs = {
            'price': {'read_only': True}
        }


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):

    orderitem = OrderItemSerializer(many=True, read_only=True, source='order')

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew',
                  'status', 'date', 'total', 'orderitem']


class UserSerilializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']