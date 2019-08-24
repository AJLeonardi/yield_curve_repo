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

    one_month_yield = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    two_month_yield = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    three_month_yield = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    six_month_yield = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    one_year_yield = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    two_year_yield = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    three_year_yield = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    five_year_yield = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    seven_year_yield = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    ten_year_yield = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    twenty_year_yield = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    thirty_year_yield = models.DecimalField(max_digits=6, decimal_places=2, default=0)

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
                return "The Yield Curve was inverted on " + self.date.strftime("%B %d, %Y")
            else:
                return "The Yield Curve was not inverted on " + self.date.strftime("%B %d, %Y")

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
        return [("1M", self.one_month_yield), ("2M", self.two_month_yield), ("3M", self.three_month_yield),
                ("6M", self.six_month_yield), ("1Y", self.one_year_yield), ("2Y", self.two_year_yield),
                ("3Y", self.three_year_yield), ("5Y", self.five_year_yield), ("7Y", self.seven_year_yield),
                ("10Y", self.ten_year_yield), ("20Y", self.twenty_year_yield), ("30Y", self.thirty_year_yield)]

    def determine_if_inverted(self):
        yield_data_list = self.yield_data_list()
        sorted_list = sorted(yield_data_list)

        return not (sorted_list == yield_data_list)

    def create_comps(self):
        yd_st_list = self.yield_data_tup_list()
        yd_lt_list = yd_st_list[1:]

        for sty in yd_st_list:
            st_rate = sty[1]
            st_label = sty[0]

            if len(yd_lt_list) > 0:
                for lty in yd_lt_list:
                    lt_rate = lty[1]
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
    rate_type = models.CharField(max_length=4, default="DTYCR", choices=TYPE_CHOICES)
    source_url = models.URLField(max_length=250, null=True, blank=True)

    long_term_yield_value = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    long_term_yield_label = models.CharField(max_length=2)

    short_term_yield_value = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    short_term_yield_label = models.CharField(max_length=2)

    yield_comp_difference = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    is_inverted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date) + " - " + self.short_term_yield_label + " : " + self.long_term_yield_label + " = " + str(self.yield_comp_difference)
