from yc_app.models import YieldData
import urllib.request
from decimal import Decimal
from datetime import datetime
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


def get_yd_from_treasury():
    # ToDo: kwargs year month and day -- if none passed, just use today's date
    url = "https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=year(NEW_DATE)%20eq%202019"
    response = urllib.request.urlopen(url).read()
    root = ET.fromstring(response)
    ns = {
        "md": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
        "d": "http://schemas.microsoft.com/ado/2007/08/dataservices",
    }
    for prop in root.iter('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        yd = YieldData()
        yd.treasury_id = int(prop.find('d:Id', ns).text)
        yd.date = datetime.strptime(prop.find("d:NEW_DATE", ns).text, "%Y-%m-%dT%H:%M:%S")
        yd.rate_type = "DTYCR"

        yd.source_url = url

        # ToDo: sometimes these are null. so this needs to accommodate for that.
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

        yd.three_month_yield = Decimal(prop.find('d:BC_3MONTH', ns).text)
        yd.six_month_yield = Decimal(prop.find('d:BC_6MONTH', ns).text)
        yd.one_year_yield = Decimal(prop.find('d:BC_1YEAR', ns).text)
        yd.two_year_yield = Decimal(prop.find('d:BC_2YEAR', ns).text)
        yd.three_year_yield = Decimal(prop.find('d:BC_3YEAR', ns).text)
        yd.five_year_yield = Decimal(prop.find('d:BC_5YEAR', ns).text)
        yd.seven_year_yield = Decimal(prop.find('d:BC_7YEAR', ns).text)
        yd.ten_year_yield = Decimal(prop.find('d:BC_10YEAR', ns).text)
        yd.twenty_year_yield = Decimal(prop.find('d:BC_20YEAR', ns).text)
        yd.thirty_year_yield = Decimal(prop.find('d:BC_30YEAR', ns).text)

        yd.is_inverted = yd.determine_if_inverted()

        try:
            yd.save()
            yd.create_comps()
        except Exception as e:
            print(e)

    return True