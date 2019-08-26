from yc_app.models import YieldData
import urllib.request
import xmltodict
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
    url = "https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%20eq%208%20and%20year(NEW_DATE)%20eq%202019"
    response = urllib.request.urlopen(url).read()
    root = ET.fromstring(response)
    for prop in root.iter('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        id = prop.find('{http://schemas.microsoft.com/ado/2007/08/dataservices}Id').text
        print(id)

    return True