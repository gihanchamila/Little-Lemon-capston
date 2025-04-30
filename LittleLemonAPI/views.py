from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the Little Lemon index.")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def secret_view(request):
    return HttpResponse("This is a secret view. Only authenticated users can see this.")