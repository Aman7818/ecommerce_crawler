# # crawler/tasks.py
#
# from celery import shared_task
# from .utils.crawler import WebCrawler
# from .models import ProductURL
#
# @shared_task
# def run_crawler_task(domains):
#     """
#     This task will run the web crawler asynchronously using Celery.
#     """
#     crawler = WebCrawler(domains)
#     product_urls = crawler.run_crawler()
#
#     # Save to DB
#     for domain, urls in product_urls.items():
#         for url in urls:
#             try:
#                 ProductURL.objects.get_or_create(domain=domain, url=url)
#             except Exception as e:
#                 print(f"Skipping duplicate URL: {url} - {str(e)}")
#
#     return product_urls
from celery import shared_task
from .utils.crawler import WebCrawler
from .models import ProductURL

@shared_task(bind=True)
def run_crawler_task(self, domain):
    """Run the web crawler for a single domain asynchronously."""
    try:
        crawler = WebCrawler([domain])  # Run crawler for one domain
        product_urls = crawler.run_crawler()

        for url in product_urls.get(domain, []):
            ProductURL.objects.get_or_create(domain=domain, url=url)

        # return {"domain": domain, "product_urls": product_urls[domain]}
        return {"domain": domain, "product_urls": product_urls.get(domain, [])}


    except Exception as e:
        self.retry(exc=e, countdown=5, max_retries=3)