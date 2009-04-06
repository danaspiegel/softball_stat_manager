from time import time

class TimerMiddleware:
    def process_request(self, request):
        request._tm_start_time = time()

    def process_response(self, request, response):
        if not hasattr(request, "_tm_start_time"):
            return

        total = time() - request._tm_start_time

        response['X-Django-Request-Time'] = '%fs' % total
        return response
