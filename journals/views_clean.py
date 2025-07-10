from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Journal


def trigger_400(request):
    return HttpResponseBadRequest("Bad request test")


def trigger_401(request):
    return HttpResponse("Unauthorized test", status=401)


def trigger_402(request):
    return HttpResponse("Payment required test", status=402)


def trigger_403(request):
    raise PermissionDenied("Forbidden test")


def trigger_404(request):
    raise Http404("Not found test")


def trigger_405(request):
    return HttpResponse("Method not allowed test", status=405)


def trigger_406(request):
    return HttpResponse("Not acceptable test", status=406)


def trigger_407(request):
    return HttpResponse("Proxy authentication required test", status=407)


def trigger_408(request):
    return HttpResponse("Request timeout test", status=408)


def trigger_409(request):
    return HttpResponse("Conflict test", status=409)


def trigger_410(request):
    return HttpResponse("Gone test", status=410)


def trigger_500(request):
    raise Exception("Server error test")


def trigger_501(request):
    return HttpResponse("Not implemented test", status=501)


def trigger_502(request):
    return HttpResponse("Bad gateway test", status=502)


def trigger_503(request):
    return HttpResponse("Service unavailable test", status=503)


def trigger_504(request):
    return HttpResponse("Gateway timeout test", status=504)


def trigger_505(request):
    return HttpResponse("HTTP version not supported test", status=505)


def dashboard(request):
    """Journal dashboard view"""
    journals = Journal.objects.all().order_by('-created_at')
    
    # Handle search and filtering
    tag_filter = request.GET.get('tag')
    search_query = request.GET.get('search')
    
    if tag_filter:
        journals = journals.filter(tags__icontains=tag_filter)
    
    if search_query:
        journals = journals.filter(
            title__icontains=search_query
        ) | journals.filter(
            content__icontains=search_query
        ) | journals.filter(
            summary__icontains=search_query
        )
    
    # Pagination
    paginator = Paginator(journals, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all unique tags for filter dropdown
    all_journals = Journal.objects.all()
    all_tags = []
    for journal in all_journals:
        if journal.tags:
            tags = [tag.strip() for tag in journal.tags.split(',')]
            all_tags.extend(tags)
    unique_tags = sorted(list(set(all_tags)))
    
    context = {
        'page_obj': page_obj,
        'journals': page_obj.object_list,
        'unique_tags': unique_tags,
        'current_tag': tag_filter,
        'search_query': search_query,
    }
    
    return render(request, 'journals/dashboard.html', context)


def journal_detail(request, pk):
    """Journal detail view"""
    journal = get_object_or_404(Journal, pk=pk)
    
    context = {
        'journal': journal,
    }
    
    return render(request, 'journals/journal_detail.html', context)


def get_tags_json(request):
    """AJAX endpoint to get all unique tags as JSON"""
    all_journals = Journal.objects.all()
    all_tags = []
    for journal in all_journals:
        if journal.tags:
            tags = [tag.strip() for tag in journal.tags.split(',')]
            all_tags.extend(tags)
    unique_tags = sorted(list(set(all_tags)))
    return JsonResponse({'tags': unique_tags})
