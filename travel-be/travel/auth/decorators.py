import functools
from django.http import HttpResponse


def auth_required(view_func):
    @functools.wraps(view_func)
    def _auth_required(request, *args, **kwargs):
        if request.token.is_valid():
            return view_func(request, *args, **kwargs)
        return HttpResponse(status=401)
    return _auth_required
