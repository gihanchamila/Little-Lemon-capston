from django.urls import path
from . import views


urlpatterns = [
    path('categories/', views.CategoryList.as_view(), name='categories'),
    path('categories/<int:pk>/', views.singleCategory.as_view(), name='single_category'),
    path('menu/', views.MenuItemList.as_view(), name='menu'),
    path('menu/<int:pk>/', views.SingleMenuItem.as_view(), name='single_menu_item'),
    path('manager/', views.ManagerList.as_view(), name='manager'),
    path('manager/<int:pk>/', views.ManagerRemove.as_view(), name='single_manager'),
    path('delivery/', views.DeliveryCrewList.as_view(), name='delivery-crew'),
    path('delivery/<int:pk>/', views.DeliveryCrewRemove.as_view(), name='single_delivery_crew'),
    path('cart/', views.CartList.as_view(), name='cart'),
    path('cart/<int:pk>/', views.SingleCartItem.as_view(), name='single_cart_item'),
]