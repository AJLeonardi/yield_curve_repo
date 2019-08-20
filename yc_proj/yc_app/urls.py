from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^DailyData/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.daily_data, name='daily_data'),

]