from django.conf.urls import url
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import YieldDataSitemap, YieldCompSitemap

sitemaps = {
    'yielddata': YieldDataSitemap,
    'yieldcomp': YieldCompSitemap,
}


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^FetchTreasuryData/$', views.FetchTreasuryData.as_view(), name='fetch_data'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.daily_data, name='daily_data'),
    url(r'^YieldComp/(?P<comp_id>\d+)/$', views.comp_page, name='comp_chart'),
    url(r'^About/', views.about_page, name='about_page'),
    url(r'^Privacy/', views.privacy_policy, name='privacy_policy'),
    url(r'^sitemap\.xml/$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

]
