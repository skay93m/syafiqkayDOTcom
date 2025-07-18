# services/error_handling.py
from django.shortcuts import render
from django.http import HttpResponseServerError
from django.http import Http404

def custom_404(request, exception):
    return render(request, '404.html', {}, status=404)

def custom_500(request):
    return HttpResponseServerError(render(request, '500.html', {}))

def trigger_error(request):
    # Deliberately raise an exception to trigger 500 error
    division_by_zero = 1 / 0
    return HttpResponse("This won't be reached")