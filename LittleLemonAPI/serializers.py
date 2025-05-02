from rest_framework import serializers
from .models import Category, MenuItem, Order, OrderItem, Cart
from django.contrib.auth.models import User

"""
    Serializers are used to convert complex data types, like querysets and model instances, into native Python datatypes.
    They also handle deserialization, allowing parsed data to be converted back into complex types.
    Serializers are similar to Django Forms, but they are not tied to any specific view or template.

    Serializers can be used to validate data, and they can also be used to create or update model instances.
    Serializers can be used to create custom fields, and they can also be used to create custom validation methods.
    
"""

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(),
        source='menuitem',
        write_only=True
    )

    class Meta:
        model = Cart
        fields = ['id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']
        read_only_fields = ['unit_price', 'price']  # prevent clients from editing these

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        menuitem = validated_data['menuitem']
        quantity = validated_data['quantity']

        # Prevent duplicates
        if Cart.objects.filter(user=user, menuitem=menuitem).exists():
            raise serializers.ValidationError("Item already in cart.")

        return Cart.objects.create(
            user=user,
            menuitem=menuitem,
            quantity=quantity
        )
    
class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']
        read_only_fields = ['unit_price', 'price']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value

    def create(self, validated_data):
        menuitem = validated_data['menuitem']
        validated_data['unit_price'] = menuitem.price
        validated_data['price'] = validated_data['unit_price'] * validated_data['quantity']
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'items']
        read_only_fields = ['total', 'date']