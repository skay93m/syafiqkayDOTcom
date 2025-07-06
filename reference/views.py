from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Reference


def coming_soon(request):
    return render(request, 'reference/coming_soon.html')


def dashboard(request):
    references = Reference.objects.all().order_by('-created_at')
    
    # Get filter parameters
    category_filter = request.GET.get('category')
    search_query = request.GET.get('search')
    
    # Apply filters
    if category_filter:
        references = references.filter(category__icontains=category_filter)
    
    if search_query:
        references = references.filter(title__icontains=search_query)
    
    # Pagination
    paginator = Paginator(references, 5)  # Show 5 references per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique categories for filtering (similar to tags)
    all_categories = []
    for reference in Reference.objects.exclude(category=''):
        if reference.category:
            cats = [cat.strip() for cat in reference.category.split(',')]
            all_categories.extend(cats)
    unique_categories = sorted(list(set(all_categories)))
    
    context = {
        'references': page_obj,
        'categories': unique_categories,
        'current_category': category_filter,
        'search_query': search_query,
    }
    return render(request, 'reference/dashboard.html', context)


def reference_detail(request, pk):
    reference = get_object_or_404(Reference, pk=pk)
    return render(request, 'reference/reference_detail.html', {'reference': reference})

def get_all_categories(request):
    """API endpoint to get all available categories"""
    all_categories = []
    for reference in Reference.objects.exclude(category=''):
        if reference.category:
            cats = [cat.strip() for cat in reference.category.split(',')]
            all_categories.extend(cats)
    
    unique_categories = sorted(list(set(all_categories)))
    return JsonResponse({'categories': unique_categories})
