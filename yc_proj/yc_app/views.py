from django.shortcuts import render
from django.shortcuts import HttpResponse


def get_context(request):
    return {"title": "State of The Yield Curve",
            "description": "The state of the yield curve for this date",
            }


def index(request):
    context = get_context(request)
    return render(request, 'yc_app/yc_data.html', context)
    #return HttpResponse("<p>Hello Django</p>")


def daily_data(request, year, month, day):
    #return render(request, 'BT_App/contact_us.html', context)
    return HttpResponse("<p>Hello Django daily data</p>")