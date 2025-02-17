# # # crawler/views.py
# #
# # import json
# # from django.http import JsonResponse
# # from django.views import View
# # from django.utils.decorators import method_decorator
# # from django.views.decorators.csrf import csrf_exempt
# # from .tasks import run_crawler_task  # Import the Celery task
# #
# # @method_decorator(csrf_exempt, name="dispatch")
# # class CrawlView(View):
# #     def post(self, request):
# #         try:
# #             data = json.loads(request.body)
# #             domains = data.get("domains", [])
# #
# #             if not domains or not isinstance(domains, list):
# #                 return JsonResponse({"error": "Invalid or missing 'domains' list in request body"}, status=400)
# #
# #             # Call Celery task instead of running the crawler synchronously
# #             task = run_crawler_task.delay(domains)  # This triggers the task asynchronously
# #
# #             return JsonResponse({"message": "Crawling started", "task_id": task.id})
# #
# #         except json.JSONDecodeError:
# #             return JsonResponse({"error": "Invalid JSON format"}, status=400)
#
#
# from django.http import JsonResponse
# from django.views import View
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .tasks import run_crawler_task  # Import Celery task
#
# @method_decorator(csrf_exempt, name="dispatch")
# class CrawlView(View):
#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             domains = data.get("domains", [])
#
#             if not domains or not isinstance(domains, list):
#                 return JsonResponse({"error": "Invalid or missing 'domains' list"}, status=400)
#
#             # Start separate tasks for each domain asynchronously
#             task_ids = []
#             for domain in domains:
#                 task = run_crawler_task.delay(domain)
#                 task_ids.append({"domain": domain, "task_id": task.id})
#
#             return JsonResponse({"tasks": task_ids, "status": "Tasks started"}, status=202)
#
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON format"}, status=400)
#
#
# from django.http import JsonResponse
# from celery.result import AsyncResult
#
# def task_status(request, task_id):
#     result = AsyncResult(task_id)
#     return JsonResponse({"task_id": task_id, "status": result.status, "result": result.result})


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
