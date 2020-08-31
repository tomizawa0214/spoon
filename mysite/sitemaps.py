from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ['index', \
                'menu', \
                'about', \
                'order_guide', \
                'order', \
                'access', \
                'contact', \
                'sctl', \
                'privacy', \
                'company', \
                'account_signup']

    def location(self, item):
        return reverse(item)