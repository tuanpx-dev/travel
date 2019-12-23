import functools
from django.http import JsonResponse


def auth_required(view_func):
    @functools.wraps(view_func)
    def _auth_required(request, *args, **kwargs):
        if request.token.is_valid():
            return view_func(request, *args, **kwargs)
        return JsonResponse(status=401)
    return _auth_required
