from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, Http404, HttpResponse
def trigger_400(request):
    return HttpResponseBadRequest("Bad request test")

def trigger_403(request):
    raise PermissionDenied("Forbidden test")

def trigger_404(request):
    raise Http404("Not found test")

def trigger_500(request):
    raise Exception("Server error test")

def trigger_501(request):
    response = HttpResponse("Not Implemented test", status=501)
    return response

def trigger_502(request):
    response = HttpResponse("Bad Gateway test", status=502)
    return response

def trigger_503(request):
    response = HttpResponse("Service Unavailable test", status=503)
    return response

def trigger_504(request):
    response = HttpResponse("Gateway Timeout test", status=504)
    return response

def trigger_505(request):
    response = HttpResponse("HTTP Version Not Supported test", status=505)
    return response

def trigger_401(request):
    response = HttpResponse("Unauthorized test", status=401)
    return response

def trigger_402(request):
    response = HttpResponse("Payment Required test", status=402)
    return response

def trigger_405(request):
    response = HttpResponse("Method Not Allowed test", status=405)
    return response

def trigger_406(request):
    response = HttpResponse("Not Acceptable test", status=406)
    return response

def trigger_407(request):
    response = HttpResponse("Proxy Authentication Required test", status=407)
    return response

def trigger_408(request):
    response = HttpResponse("Request Timeout test", status=408)
    return response

def trigger_409(request):
    response = HttpResponse("Conflict test", status=409)
    return response

def trigger_410(request):
    response = HttpResponse("Gone test", status=410)
    return response
from django.shortcuts import render, get_object_or_404
from .models import Journal

def coming_soon(request):
    return render(request, 'journals/coming_soon.html')

def dashboard(request):
    journals = Journal.objects.all().order_by('-created_at')
    return render(request, 'journals/dashboard.html', {'journals': journals})

def journal_detail(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    return render(request, 'journals/journal_detail.html', {'journal': journal})