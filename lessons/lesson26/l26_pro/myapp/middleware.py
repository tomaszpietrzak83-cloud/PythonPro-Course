# TASK 07
class SimpleMethodMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print(f"Request method:: {request.method}")

        response = self.get_response(request)

        print(f"Status: {response.status_code}")

        return response
