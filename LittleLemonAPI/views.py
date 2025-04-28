from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the Little Lemon index.")