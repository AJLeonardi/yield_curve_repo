from django.shortcuts import render
from django.shortcuts import HttpResponse
from yc_app import helpers
from django.utils import timezone


def get_context(request):
    return {"title": "State of The Yield Curve",
            "description": "The state of the yield curve for this date",
            }


def index(request):
    context = get_context(request)
    current_yd = helpers.get_yd_by_date(timezone.now().date())
    context['yd'] = current_yd
    context['yd_inversion_string_short'] = current_yd.yd_inversion_string_short()
    context['yd_comps'] = current_yd.yield_comps.all()
    return render(request, 'yc_app/yc_data.html', context)
    #return HttpResponse("<p>Hello Django</p>")


def daily_data(request, year, month, day):
    #return render(request, 'BT_App/contact_us.html', context)
    return HttpResponse("<p>Hello Django daily data</p>")