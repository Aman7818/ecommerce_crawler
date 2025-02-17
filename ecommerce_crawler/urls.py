from django.urls import path
# from .views import CrawlView
from crawler.views import CrawlView

urlpatterns = [
    path('crawl/', CrawlView.as_view(), name='crawl'),
    # path('task_status/<str:task_id>/', task_status, name='task_status'),
]
