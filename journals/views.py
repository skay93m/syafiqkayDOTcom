from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, Http404
def trigger_400(request):
    return HttpResponseBadRequest("Bad request test")

def trigger_403(request):
    raise PermissionDenied("Forbidden test")

def trigger_404(request):
    raise Http404("Not found test")

def trigger_500(request):
    raise Exception("Server error test")
from django.shortcuts import render, get_object_or_404
from .models import Journal

def coming_soon(request):
    pass

def dashboard(request):
    journals = Journal.objects.all().order_by('-created_at')
    return render(request, 'journals/dashboard.html', {'journals': journals})

def journal_detail(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    return render(request, 'journals/journal_detail.html', {'journal': journal})