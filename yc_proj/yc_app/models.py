from django.db import models
from django.shortcuts import reverse

# Create your models here.


class YieldData(models.Model):
    treasury_id = models.IntegerField(unique=True)
    date = models.DateTimeField('Date for Treasury Yield Data')
    is_inverted = models.BooleanField(default=False)
    data_source = models.CharField(max_length=100, default="U.S. Treasury")

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
        return str(self.date.year) + "-" + str(self.date.month) + "-" + str(self.date.day)

    def get_absolute_url(self):
        year = self.date.year
        month = self.date.month
        day = self.date.day
        return reverse('yc_app:daily_data', args=[year, month, day])

    class Meta:
        ordering = ['-date']
