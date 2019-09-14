from django.db import models
from django.shortcuts import reverse
from django.utils import timezone

# Create your models here.
TYPE_CHOICES = (
    ('DTYCR', "Daily Treasury Yield Curve Rates"),
    ('DTRYCR', 'Daily Treasury Real Yield Curve Rates'),
)


class YieldData(models.Model):
    treasury_id = models.IntegerField(unique=True)
    date = models.DateTimeField('Date for Treasury Yield Data')
    rate_type = models.CharField(max_length=10, default="DTYCR", choices=TYPE_CHOICES)

    is_inverted = models.BooleanField(default=False)
    data_source = models.CharField(max_length=100, default="U.S. Department of the Treasury")
    source_url = models.URLField(max_length=250, null=True, blank=True)

    one_month_yield = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    two_month_yield = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    three_month_yield = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    six_month_yield = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    one_year_yield = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    two_year_yield = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    three_year_yield = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    five_year_yield = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    seven_year_yield = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    ten_year_yield = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    twenty_year_yield = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    thirty_year_yield = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.date.year) + "-" + str(self.date.month) + "-" + str(self.date.day) + " - is_inverted: " + str(self.is_inverted)

    def yd_inversion_string_short(self):
        try:
            self.get_next_by_date()
            is_latest = False
        except YieldData.DoesNotExist:
            is_latest = True

        if is_latest:
            if self.is_inverted:
                return "The Yield Curve is inverted"
            else:
                return "The Yield Curve is not inverted"
        else:
            if self.is_inverted:
                return "The Yield Curve was inverted"
            else:
                return "The Yield Curve was not inverted"

    def get_absolute_url(self):
        year = self.date.year
        month = self.date.strftime('%m')
        day = self.date.strftime('%d')
        return reverse('yc_app:daily_data', args=[year, month, day])

    def yield_data_list(self):
        return [self.one_month_yield, self.two_month_yield, self.three_month_yield, self.six_month_yield,
                self.one_year_yield, self.two_year_yield, self.three_year_yield, self.five_year_yield,
                self.seven_year_yield, self.ten_year_yield, self.twenty_year_yield, self.thirty_year_yield]

    def yield_data_tup_list(self):
        return [("1M", self.one_month_yield), ("2M", self.two_month_yield),
                ("3M", self.three_month_yield), ("6M", self.six_month_yield),
                ("1Y", self.one_year_yield), ("2Y", self.two_year_yield),
                ("3Y", self.three_year_yield), ("5Y", self.five_year_yield),
                ("7Y", self.seven_year_yield), ("10Y", self.ten_year_yield),
                ("20Y", self.twenty_year_yield), ("30Y", self.thirty_year_yield)]

    def determine_if_inverted(self):
        yield_data_list = self.yield_data_list()
        yield_data_list = [x for x in yield_data_list if x is not None]
        sorted_list = sorted(yield_data_list)

        return not (sorted_list == yield_data_list)

    def get_comp_grid(self):
        comp_list = list(self.yield_comps.all())
        header = [None,"2M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]
        durations = ["1M","2M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]
        first_row = []
        for h in header:
            if h is None:
                label = ""
            else:
                label = h
            first_row.append({
                'label': label,
                'object': None,
                'is_header': True,
            })
        grid = [first_row]

        for std in durations:
            if std is not None and std is not "30Y":
                row = [{
                    'label': std,
                    'object': None,
                    'is_header': True,
                    'state': 'header',
                    'drill_down_url': False,
                }]
                for ltd in durations:
                    if ltd is not None and ltd is not "1M":
                        try:
                            comp = [x for x in comp_list if x.short_term_yield_label == std and  x.long_term_yield_label == ltd][0]
                            if comp.is_inverted:
                                state = "inverted"
                            elif comp.yield_comp_difference == 0:
                                state = "even"
                            else:
                                state = "normal"

                            row.append({
                                'label': str(comp),
                                'object': comp,
                                'is_header': False,
                                'state': state,
                                'drill_down_url': comp.get_absolute_url(),
                                })
                        except Exception as e:
                            row.append({
                                'label': "--",
                                'object': None,
                                'is_header': False,
                                'state': "na",
                                'drill_down_url': False,
                            })
                grid.append(row)
        return grid

    def create_comps(self):
        yd_st_list = self.yield_data_tup_list()
        yd_lt_list = yd_st_list[1:]

        for sty in yd_st_list:
            st_rate = sty[1]
            st_label = sty[0]
            if st_rate is not None:
                if len(yd_lt_list) > 0:
                    for lty in yd_lt_list:
                        lt_rate = lty[1]
                        if lt_rate is not None:
                            yc_diff = lt_rate - st_rate
                            is_yc_inverted = (yc_diff < 0)
                            yc = YieldComp(yield_data=self, date=self.date, rate_type=self.rate_type, source_url=self.source_url,
                                           long_term_yield_value=lt_rate, long_term_yield_label=lty[0],
                                           short_term_yield_value=st_rate, short_term_yield_label=st_label,
                                           yield_comp_difference=yc_diff, is_inverted=is_yc_inverted)
                            yc.save()

                    del yd_lt_list[0]

    class Meta:
        ordering = ['-date']


class YieldComp(models.Model):
    yield_data = models.ForeignKey(YieldData, related_name="yield_comps")
    date = models.DateTimeField('Date for Treasury Yield Data')
    rate_type = models.CharField(max_length=6, default="DTYCR", choices=TYPE_CHOICES)
    source_url = models.URLField(max_length=250, null=True, blank=True)

    long_term_yield_value = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    long_term_yield_label = models.CharField(max_length=4)

    short_term_yield_value = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    short_term_yield_label = models.CharField(max_length=4)

    yield_comp_difference = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    is_inverted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('rate_type', 'date', 'short_term_yield_label', 'long_term_yield_label')

    def __str__(self):
        return str(self.yield_comp_difference)

    def get_absolute_url(self):
        comp_id = self.pk
        return reverse('yc_app:comp_chart', args=[comp_id])