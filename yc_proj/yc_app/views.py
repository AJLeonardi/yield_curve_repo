import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
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
    context['is_latest_yd'] = True # TODO: convert this to has_next
    context['yd_inversion_string_short'] = current_yd.yd_inversion_string_short()
    context['yd_comps'] = current_yd.yield_comps.all()
    return render(request, 'yc_app/yc_data.html', context)


def daily_data(request, year, month, day):
    date = datetime.datetime(year=int(year), month=int(month), day=int(day))
    current_yd = helpers.get_yd_by_date(date)
    today = timezone.now().date()

    if current_yd.date.date() == today:
        return HttpResponseRedirect(reverse('yc_app:index', kwargs={}))

    if current_yd.date.date() == date.date():
        context = get_context(request)
        context['yd'] = current_yd
        context['is_latest_yd'] = False # TODO: convert this to has_next
        context['yd_inversion_string_short'] = current_yd.yd_inversion_string_short()
        context['yd_comps'] = current_yd.yield_comps.all()
        return render(request, 'yc_app/yc_data.html', context)
    else:
        return HttpResponseRedirect(reverse('yc_app:daily_data', kwargs={'year': current_yd.date.strftime('%Y'),
                                                                         'month': current_yd.date.strftime('%m'),
                                                                         'day': current_yd.date.strftime('%d')}))
