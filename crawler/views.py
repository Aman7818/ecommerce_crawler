from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import threading
from .utils.crawler import WebCrawler

@method_decorator(csrf_exempt, name="dispatch")
class CrawlView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            domains = data.get("domains", [])

            if not domains or not isinstance(domains, list):
                return JsonResponse({"error": "Invalid or missing 'domains' list"}, status=400)

            def start_crawling(domain):
                crawler = WebCrawler([domain])
                product_urls = crawler.run_crawler()
                print(f"Crawling completed for {domain}: {product_urls}")

            # Start a separate thread for each domain
            for domain in domains:
                thread = threading.Thread(target=start_crawling, args=(domain,))
                thread.start()

            return JsonResponse({"message": "Crawling started in background"}, status=202)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class ScrapeView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            domains = data.get("domains", [])

            if not domains or not isinstance(domains, list):
                return JsonResponse({"error": "Invalid or missing 'domains' list"}, status=400)

            crawler = WebCrawler(domains)
            scraped_data = crawler.run_crawler()

            return JsonResponse({"message": "Crawling completed", "data": scraped_data}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)