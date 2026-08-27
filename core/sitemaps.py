from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        # List all named URL patterns you want to include
        return [
            'prelimspage',
            'cfa_step1',
            'cfa_step2',
            'cfa_step3',
            # ...add more named views from your urls.py if desired
        ]

    def location(self, item):
        return reverse(item)
