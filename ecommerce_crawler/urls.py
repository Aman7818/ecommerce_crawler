from django.urls import path
# from .views import CrawlView
from crawler.views import CrawlView, ScrapeView

urlpatterns = [
    path('crawl/', CrawlView.as_view(), name='crawl'),
    path('scrape/', ScrapeView.as_view(), name='scrape'),
]
