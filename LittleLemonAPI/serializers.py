from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User
from decimal import Decimal

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

        def validate_name(self, value):
            # Prevent duplicate category names (case-insensitive)
            if Category.objects.filter(name__iexact=value).exists():
                raise serializers.ValidationError("A category with this name already exists.")
            return value

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
        # Convert unit_price to Decimal if it's a string
        unit_price = Decimal(attrs['unit_price'])
        quantity = attrs['quantity']
        attrs['price'] = unit_price * quantity
        return attrs

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'unit_price', 'quantity', 'price']
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

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['delivery_crew', 'status']

        def validate_delivery_crew(self, value):
            if not value.groups.filter(name='delivery crew').exists():
                raise serializers.ValidationError("Assigned user must be in the delivery crew group.")
            return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']