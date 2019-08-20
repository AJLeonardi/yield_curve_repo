from django.shortcuts import render
from django.shortcuts import HttpResponse


def index(request):
    return HttpResponse("<p>Hello Django</p>")


def daily_data(request, year, month, day):
    return HttpResponse("<p>Hello Django daily data</p>")