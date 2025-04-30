from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('secret/', views.secret_view, name='secret_view'),
]