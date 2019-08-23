import datetime
import yc_app
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from yc_app import helpers
from django.utils import timezone


def get_context(request, yd):
    context = {"title": "State of The Yield Curve",
               "description": "The state of the yield curve for this date",
               'yd': yd,}
    try:
        next_yd = yd.get_next_by_date()
        context['is_latest_yd'] = False
        context['next_yd_url'] = next_yd.get_absolute_url()
    except yc_app.models.YieldData.DoesNotExist:
        context['next_yd_url'] = "#"
        context['is_latest_yd'] = True

    try:
        prev_yd = yd.get_previous_by_date()
        context['is_first_yd'] = False
        context['prev_yd_url'] = prev_yd.get_absolute_url()
    except yc_app.models.YieldData.DoesNotExist:
        context['prev_yd_url'] = "#"
        context['is_first_yd'] = True

    context['yd_inversion_string_short'] = yd.yd_inversion_string_short()
    context['yd_comps'] = yd.yield_comps.all()

    return context


def index(request):
    current_yd = helpers.get_yd_by_date(timezone.now().date())
    context = get_context(request, current_yd)
    return render(request, 'yc_app/yc_data.html', context)


def daily_data(request, year, month, day):
    date = datetime.datetime(year=int(year), month=int(month), day=int(day))
    current_yd = helpers.get_yd_by_date(date)

    if current_yd.date.date() == date.date():
        context = get_context(request, current_yd)
        return render(request, 'yc_app/yc_data.html', context)
    else:
        return HttpResponseRedirect(reverse('yc_app:daily_data', kwargs={'year': current_yd.date.strftime('%Y'),
                                                                         'month': current_yd.date.strftime('%m'),
                                                                         'day': current_yd.date.strftime('%d')}))
