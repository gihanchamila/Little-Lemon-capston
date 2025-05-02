
import math
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group
from decimal import Decimal

from .models import MenuItem, Cart, Order, OrderItem
from .serializers import UserSerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from .permissions import IsManager
from .paginations import MenuItemListPagination, OrderListPagination, CartListPagination

# Create your views here.

class MenuItemsList(generics.ListCreateAPIView):

    """
    List all menu items or create a new one.
    Only managers can create new menu items
    and only authenticated users can view the list.
    The list is paginated and can be filtered by title and category.
    The results can be ordered by title and price.
    The API is rate-limited to 10 requests per minute for authenticated users
    and 5 requests per minute for anonymous users.

    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    search_fields = ['title', 'category__title']
    ordering_fields = ['title', 'price']
    pagination_class = MenuItemListPagination

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
                permission_classes = [IsAuthenticated,IsManager]
        return[permission() for permission in permission_classes]
    
class MenuItemDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a menu item.
    Only managers can update or delete menu items.
    The item can be retrieved by its ID.
    The API is rate-limited to 10 requests per minute for authenticated users
    and 5 requests per minute for anonymous users.

    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
                permission_classes = [IsAuthenticated,IsManager]
        return[permission() for permission in permission_classes]
    
class ManagerList(generics.ListCreateAPIView):
    """
    List all users in the Manager group or add a new user to the Manager group.
    Only authenticated users with the Manager group can access this view.
    The API is rate-limited to 10 requests per minute for authenticated users
    and 5 requests per minute for anonymous users.

    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')

        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        if user.groups.filter(name='Manager').exists():
            return JsonResponse({'error': 'User is already a manager'}, status=400)

        group = Group.objects.get(name='Manager')
        user.groups.add(group)
        return JsonResponse({'message': 'User added to Manager group'}, status=201)

class ManagerRemove(generics.DestroyAPIView):
    """
    Remove a user from the Manager group.
    Only authenticated users with the Manager group can access this view.
    The API is rate-limited to 10 requests per minute for authenticated users
    and 5 requests per minute for anonymous users.
    
    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def delete(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        if not user.groups.filter(name='Manager').exists():
            return JsonResponse({'error': 'User is not a manager'}, status=400)

        group = Group.objects.get(name='Manager')
        user.groups.remove(group)
        return JsonResponse({'message': 'User removed from Manager group'}, status=200)
     
class DeliveryCrewList(generics.ListCreateAPIView):
    """
    List all users in the Delivery Crew group or add a new user to the Delivery Crew group.
    Only authenticated users with the Manager group can access this view.
    The API is rate-limited to 10 requests per minute for authenticated users
    and 5 requests per minute for anonymous users.
    
    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = User.objects.filter(groups__name='Delivery Crew')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager]


    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        if user.groups.filter(name='Delivery Crew').exists():
            return JsonResponse({'error': 'User is already a delivery crew member'}, status=400)

        try:
            group = Group.objects.get(name='Delivery Crew')
        except Group.DoesNotExist:
            return JsonResponse({'error': 'Delivery Crew group does not exist'}, status=404)

        user.groups.add(group)
        return JsonResponse({'message': 'User added to Delivery Crew group'}, status=201)
    
class DeliveryCrewRemove(generics.DestroyAPIView):
    """
    Remove a user from the Delivery Crew group.
    Only authenticated users with the Manager group can access this view.
    The API is rate-limited to 10 requests per minute for authenticated users
    and 5 requests per minute for anonymous users.
        
    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = User.objects.filter(groups__name='Delivery Crew')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def delete(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        if not user.groups.filter(name='Delivery Crew').exists():
            return JsonResponse({'error': 'User is not a delivery crew member'}, status=400)

        group = Group.objects.get(name='Delivery Crew')
        user.groups.remove(group)
        return JsonResponse({'message': 'User removed from Delivery crew group'}, status=200)
    
class CartOperationsView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    """
    List all items in the cart or add a new item to the cart.
    Update the quantity of an item in the cart or delete an item from the cart.
    Only authenticated users can access this view.
    The API is rate-limited to 10 requests per minute for authenticated users
    and 5 requests per minute for anonymous users.
    
    """
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['menuitem__title']
    ordering_fields = ['menuitem__title', 'quantity']
    pagination_class = CartListPagination

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        menuitem_id = request.data.get('menuitem_id')
        quantity = request.data.get('quantity')

        if not menuitem_id or not quantity:
            return JsonResponse({'error': 'Menu item ID and quantity are required'}, status=400)

        try:
            menuitem = MenuItem.objects.get(id=menuitem_id)
        except MenuItem.DoesNotExist:
            return JsonResponse({'error': 'Menu item does not exist'}, status=404)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            menuitem=menuitem,
            defaults={'quantity': quantity, 'unit_price': menuitem.price}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({'message': f"Cart updated successfully, {cart_item.quantity}"}, status=201)


    def put(self, request, *args, **kwargs):
        menuitem_id = request.data.get('menuitem_id')
        quantity = request.data.get('quantity')

        if not menuitem_id or not quantity:
            return JsonResponse({'error': 'Menu item ID and quantity are required'}, status=400)

        try:
            menuitem = MenuItem.objects.get(id=menuitem_id)
        except MenuItem.DoesNotExist:
            return JsonResponse({'error': 'Menu item does not exist'}, status=404)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            menuitem=menuitem,
            defaults={'quantity': quantity, 'unit_price': menuitem.price}
        )

        if not created:
            cart_item.quantity = quantity
            cart_item.save()

        return Response({'message': f"Cart updated successfully, {quantity}"}, status=200)

    def delete(self, request, *args, **kwargs):
        menuitem_id = request.data.get('menuitem_id')

        if menuitem_id:
            # Delete one specific item
            cart_item = get_object_or_404(
                Cart,
                user=request.user,
                menuitem__id=menuitem_id
            )
            cart_item.delete()
            return Response({'message': 'Item removed from cart'}, status=200)
        else:
            # Delete all items
            Cart.objects.filter(user=request.user).delete()
            return Response({'message': 'All items removed from cart'}, status=200)

class OrderList(generics.ListCreateAPIView):
    """
    List all orders or create a new order.
    Only authenticated users can create new orders.
    The list is paginated and can be filtered by user and status.
    The results can be ordered by user and status.
    The API is rate-limited to 10 requests per minute for authenticated users
    and 5 requests per minute for anonymous users.

    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['user__username', 'status']
    ordering_fields = ['user__username', 'status']
    pagination_class = OrderListPagination

    def get_queryset(self, *args, **kwargs):
        if self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_superuser:
            query = Order.objects.all()
        elif self.request.user.groups.filter(name='Delivery Crew').exists():
            query = Order.objects.filter(delivery_crew=self.request.user)
        else:
            query = Order.objects.filter(user=self.request.user)
        return query
    
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]

        return [permission() for permission in permission_classes]
    
    def post(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=400)

        order = Order.objects.create(user=request.user, total=Decimal('0.00'))

        order_items = []
        total = Decimal('0.00')

        for item in cart_items:
            order_items.append(OrderItem(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            ))
            total += item.price

        OrderItem.objects.bulk_create(order_items)

        order.total = total
        order.save()

        cart_items.delete() #

        return Response({'message': 'Order created successfully', 'order_id': order.id}, status=201)
    
class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an order.
    Only authenticated users can retrieve their own orders.
    Only managers can update or delete orders.
    The order can be retrieved by its ID.
    The API is rate-limited to 10 requests per minute for authenticated users
    and 5 requests per minute for anonymous users.

    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    
    def put(self, request, *args, **kwargs):
        order = self.get_object()
        is_manager = request.user.groups.filter(name='Manager').exists()

        if order.user != request.user and not is_manager:
            return Response({'error': 'You do not have permission to update this order'}, status=403)
        

        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
    
    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        is_manager = request.user.groups.filter(name='Manager').exists()

        if not (is_manager or request.user.is_superuser):
            return Response({'error': 'You do not have permission to delete this order'}, status=403)

        order.delete()
        return Response(status=204)