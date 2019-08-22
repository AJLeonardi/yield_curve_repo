from yc_app.models import YieldData
from datetime import timedelta


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

