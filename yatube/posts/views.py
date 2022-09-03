from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Главная страница')

def group_posts(request):
    return HttpResponse('Доступные гурппы')

# Create your views here.
