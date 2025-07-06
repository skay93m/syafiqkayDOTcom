from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
<<<<<<< HEAD
from django.core.paginator import Paginator
=======
>>>>>>> 324dc61 (Refactor journal and reference models to support tags and categories)
from .models import Journal

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

def coming_soon(request):
    return render(request, 'journals/coming_soon.html')

def dashboard(request):
    journals = Journal.objects.all().order_by('-created_at')
    
    # Get filter parameters
    author_filter = request.GET.get('author')
<<<<<<< HEAD
<<<<<<< HEAD
    tag_filter = request.GET.get('tag')
=======
>>>>>>> af068c0 (Add Noto Garden dashboard, graph, guide, note detail, and note form templates)
=======
    tag_filter = request.GET.get('tag')
>>>>>>> 324dc61 (Refactor journal and reference models to support tags and categories)
    search_query = request.GET.get('search')
    
    # Apply filters
    if author_filter:
        journals = journals.filter(author__username=author_filter)
    
<<<<<<< HEAD
<<<<<<< HEAD
    if tag_filter:
        journals = journals.filter(tags__icontains=tag_filter)
    
    if search_query:
        journals = journals.filter(title__icontains=search_query)
    
    # Pagination
    paginator = Paginator(journals, 5)  # Show 5 journals per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique authors for filtering
    authors = Journal.objects.values_list('author__username', flat=True).distinct()
    
    # Get unique tags for filtering
    all_tags = []
    for journal in Journal.objects.exclude(tags=''):
        if journal.tags:
            tags = [tag.strip() for tag in journal.tags.split(',')]
            all_tags.extend(tags)
    unique_tags = sorted(list(set(all_tags)))
    
    context = {
        'journals': page_obj,
        'authors': authors,
        'tags': unique_tags,
        'current_author': author_filter,
        'current_tag': tag_filter,
=======
=======
    if tag_filter:
        journals = journals.filter(tags__icontains=tag_filter)
    
>>>>>>> 324dc61 (Refactor journal and reference models to support tags and categories)
    if search_query:
        journals = journals.filter(title__icontains=search_query)
    
    # Get unique authors for filtering
    authors = Journal.objects.values_list('author__username', flat=True).distinct()
    
    # Get unique tags for filtering
    all_tags = []
    for journal in Journal.objects.exclude(tags=''):
        if journal.tags:
            tags = [tag.strip() for tag in journal.tags.split(',')]
            all_tags.extend(tags)
    unique_tags = sorted(list(set(all_tags)))
    
    context = {
        'journals': journals,
        'authors': authors,
        'tags': unique_tags,
        'current_author': author_filter,
<<<<<<< HEAD
>>>>>>> af068c0 (Add Noto Garden dashboard, graph, guide, note detail, and note form templates)
=======
        'current_tag': tag_filter,
>>>>>>> 324dc61 (Refactor journal and reference models to support tags and categories)
        'search_query': search_query,
    }
    return render(request, 'journals/dashboard.html', context)

def journal_detail(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    return render(request, 'journals/journal_detail.html', {'journal': journal})

def get_all_tags(request):
    """API endpoint to get all available tags"""
    all_tags = []
    for journal in Journal.objects.exclude(tags=''):
        if journal.tags:
            tags = [tag.strip() for tag in journal.tags.split(',')]
            all_tags.extend(tags)
    
    unique_tags = sorted(list(set(all_tags)))
    return JsonResponse({'tags': unique_tags})