# decorators.py

from functools import wraps

def ensure_200_status(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response.status_code = 200
        return response
    return wrapper
