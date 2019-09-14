from yc_app.models import YieldData, YieldComp
import urllib.request
from datetime import datetime
from decimal import Decimal
import datetime
import xml.etree.ElementTree as ET


def get_yd_by_date(date):
    # should not be a datetime object

    try:
        return YieldData.objects.get(date__date=date)

    except YieldData.DoesNotExist:
        yd_list = YieldData.objects.filter(date__date__lte=date).order_by("-date")

        if yd_list.count() > 0:
            return yd_list[0]

        else:
            return YieldData.objects.filter(date__date__gte=date).order_by("date")[0]


def get_yd_from_treasury(year, month=None, day=None ):
    url = "https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=year(NEW_DATE)%20eq%20" + str(year)
    if month:
        url += "%20and%20month(NEW_DATE)%20eq%20" + str(month)
        if day:
            url += "%20and%20day(NEW_DATE)%20eq%20" + str(day)
    response = urllib.request.urlopen(url).read()
    root = ET.fromstring(response)
    ns = {
        "md": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
        "d": "http://schemas.microsoft.com/ado/2007/08/dataservices",
    }
    for prop in root.iter('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        yd = YieldData()
        yd.treasury_id = int(prop.find('d:Id', ns).text)
        yd.date = datetime.datetime.strptime(prop.find("d:NEW_DATE", ns).text, "%Y-%m-%dT%H:%M:%S")
        yd.rate_type = "DTYCR"

        yd.source_url = url

        omy = prop.find('d:BC_1MONTH', ns).text
        if omy:
            yd.one_month_yield = Decimal(omy)
        else:
            yd.one_month_yield = None

        tmy = prop.find('d:BC_2MONTH', ns).text
        if tmy:
            yd.two_month_yield = Decimal(tmy)
        else:
            yd.two_month_yield = None

        threemy = prop.find('d:BC_3MONTH', ns).text
        if threemy:
            yd.three_month_yield = Decimal(threemy)
        else:
            yd.three_month_yield = None

        sixmy = prop.find('d:BC_6MONTH', ns).text
        if sixmy:
            yd.six_month_yield = Decimal(sixmy)
        else:
            yd.six_month_yield = None

        oneyy = prop.find('d:BC_1YEAR', ns).text
        if oneyy:
            yd.one_year_yield = Decimal(oneyy)
        else:
            yd.one_year_yield = None

        twoyy = prop.find('d:BC_2YEAR', ns).text
        if twoyy:
            yd.two_year_yield = Decimal(twoyy)
        else:
            yd.two_year_yield = None

        threeyy = prop.find('d:BC_3YEAR', ns).text
        if threeyy:
            yd.three_year_yield = Decimal(threeyy)
        else:
            yd.three_year_yield = None

        fiveyy = prop.find('d:BC_5YEAR', ns).text
        if fiveyy:
            yd.five_year_yield = Decimal(fiveyy)
        else:
            yd.five_year_yield = None

        sevenyy = prop.find('d:BC_7YEAR', ns).text
        if sevenyy:
            yd.seven_year_yield = Decimal(sevenyy)
        else:
            yd.seven_year_yield = None

        tenyy = prop.find('d:BC_10YEAR', ns).text
        if tenyy:
            yd.ten_year_yield = Decimal(tenyy)
        else:
            yd.ten_year_yield = None

        twentyyy = prop.find('d:BC_20YEAR', ns).text
        if twentyyy:
            yd.twenty_year_yield = Decimal(twentyyy)
        else:
            yd.twenty_year_yield = None

        thirtyyy = prop.find('d:BC_30YEAR', ns).text
        if thirtyyy:
            yd.thirty_year_yield = Decimal(thirtyyy)
        else:
            yd.thirty_year_yield = None

        yd.is_inverted = yd.determine_if_inverted()

        try:
            yd.save()
            yd.create_comps()
        except Exception as e:
            print(e)

    return True


def get_comp_chart_list(comp_id, num_days_of_data):
    comp = YieldComp.objects.get(pk=comp_id)
    start_date = comp.date - datetime.timedelta(days=num_days_of_data)
    return comp.short_term_yield_label, comp.long_term_yield_label, list(YieldComp.objects.filter(date__gte=start_date,
                                                                                                  date__lte=comp.date,
                                                                                                  rate_type=comp.rate_type,
                                                                                                  long_term_yield_label=comp.long_term_yield_label,
                                                                                                  short_term_yield_label=comp.short_term_yield_label).order_by('date'))
