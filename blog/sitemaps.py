# this file is for the search engines

from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    # The changefreq and priority attributes indicate the change frequesncy of your post pages and their relevance in your website(max val is 1)
    changefreq = 'weekly'
    priority = 0.9

    # The items() method returns the queryset of the objects to include in this sitemap.
    # By default django calls the get_absolute_url() method on each object to retrieve its URL
    def items(self):
        return Post.published.all()
    
    # The lastmod method recieves each object returned by items() and returns the last time the object was modified.
    def lastmod(self, obj):
        return obj.updated_at