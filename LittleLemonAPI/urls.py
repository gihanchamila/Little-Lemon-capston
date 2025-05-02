from django.urls import path
from . import views


urlpatterns = [
    path('menu-items', views.MenuItemsList.as_view(), name='menu-list'),
    path('menu-items/<int:pk>', views.MenuItemDetail.as_view(), name='menu-detail'),
    path('groups/manager/users', views.ManagerList.as_view(), name='manager-list'),
    path('groups/manager/users/<int:pk>', views.ManagerRemove.as_view(), name='manager-remove'),
    path('groups/delivery-crew/users', views.DeliveryCrewList.as_view(), name='delivery-crew-list'),
    path('groups/delivery-crew/<int:pk>', views.DeliveryCrewRemove.as_view(), name='delivery-crew-remove'),
    path('cart/menu-items', views.CartOperationsView.as_view(), name='cart-menu-list'),
    path('orders', views.OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>', views.OrderDetail.as_view(), name='order-detail'),
]