from django.http.response import JsonResponse

class ErrorResponse(JsonResponse):
    def __init__(self, message=None, status=400):
        temp = {
            "errors": [message]
        }
        super(ErrorResponse, self).__init__(temp, status=status)