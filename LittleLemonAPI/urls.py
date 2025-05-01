from django.urls import path
from . import views


urlpatterns = [
    path('menu-items/', views.MenuItemList.as_view(), name='menu-list'),
    path('menu-items/<int:pk>/', views.MenuItemDetail.as_view(), name='menu-detail'),
]