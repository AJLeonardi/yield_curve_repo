import datetime
import yc_app
from yc_app import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from yc_app import helpers
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


def get_context(request, yd):
    context = {"title": "State of The Yield Curve",
               "description": "The state of the yield curve for this date",
               'obj': yd,
               'is_comp': False,
               }
    try:
        next_yd = yd.get_next_by_date()
        context['is_latest_yd'] = False
        context['next_yd_url'] = next_yd.get_absolute_url()
    except (AttributeError, yc_app.models.YieldData.DoesNotExist):
        context['next_yd_url'] = "#"
        context['is_latest_yd'] = True

    try:
        prev_yd = yd.get_previous_by_date()
        context['is_first_yd'] = False
        context['prev_yd_url'] = prev_yd.get_absolute_url()
    except (AttributeError, yc_app.models.YieldData.DoesNotExist):
        context['prev_yd_url'] = "#"
        context['is_first_yd'] = True
    try:
        context['yd_inversion_string_short'] = yd.yd_inversion_string_short()
        context['yd_comp_grid'] = yd.get_comp_grid()
    except AttributeError:
        context['yd_inversion_string_short'] = ""
        context['yd_comp_grid'] = ""

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


def comp_page(request, comp_id):
    date_range = int(request.GET.get('date_range', '365'))
    sty_label, lty_label, chart_list = helpers.get_comp_chart_list(comp_id, date_range)
    comp = chart_list[-1:][0]
    # daily_yd = comp.yield_data.get_absolute_url()
    chart_data = []
    for comp in chart_list:
        comp_tup = comp.date.strftime("%m/%d/%Y"), comp.yield_comp_difference
        chart_data.append(comp_tup)
    context = {
        "chart_label": "Yield Comparison " + sty_label + ":" + lty_label,
        "chart_data": chart_data,
        "sty_label": sty_label,
        "lty_label": lty_label,
        "obj": comp,
        "title": "Yield Comparison " + sty_label + ":" + lty_label,
        'daily_data_url': comp.yield_data.get_absolute_url(),
        "description": "The comparison of the " + sty_label + " and " + lty_label
                       + "yields. A negative value here shows an inversion of the yield curve.",
        'is_comp': True,
        'date_range': date_range,
    }
    return render(request, 'yc_app/comp_chart.html', context)


class FetchTreasuryData(LoginRequiredMixin, View):

    def get(self, request):
        context = get_context(request, None)
        context['form'] = forms.FetchTreasuryDataForm()
        return render(request, 'yc_app/fetch_treasury_data.html', context)

    def post(self, request):
        form = forms.FetchTreasuryDataForm(request.POST or None)
        if form.is_valid():
            helpers.get_yd_from_treasury(form.cleaned_data['year'], month=form.cleaned_data['month'],
                                         day=form.cleaned_data['day'])
        return HttpResponseRedirect(reverse('yc_app:index'))


def get_static_context(request, page_name, description):
    return {
        "title": "State of The Yield Curve - " + page_name,
        'description': description,
        'daily_data_url': reverse('yc_app:index'),
        'is_comp': True,
        }


def about_page(request):
    context = get_static_context(request, 'About', "The State of The Yield Curve provides daily details on the US treasury Yield Curve and the context around that single data point.")

    return render(request, 'yc_app/about.html', context)


def privacy_policy(request):
    context = get_static_context(request, 'Privacy', "The State of The Yield Curve's Privacy Notice.")

    return render(request, 'yc_app/privacy.html', context)