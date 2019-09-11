from django.contrib import sitemaps
from yc_app.models import YieldComp, YieldData


class YieldDataSitemap(sitemaps.Sitemap):
    priority = 0.9
    changefreq = 'daily'
    limit = 50000

    def items(self):
        return YieldData.objects.all()

    def location(self, item):
        return item.get_absolute_url()


class YieldCompSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'
    limit = 10000

    def items(self):
        return YieldComp.objects.all()

    def location(self, item):
        return item.get_absolute_url()