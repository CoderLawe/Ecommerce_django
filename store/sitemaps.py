from django.contrib.sitemaps import Sitemap
from .models import Product

class ProductSiteMap(Sitemap):
    def items(self):
        return Product.objects.all()
