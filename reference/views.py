from django.shortcuts import render, get_object_or_404
from .models import Reference


def coming_soon(request):
    return render(request, 'reference/coming_soon.html')


def dashboard(request):
    references = Reference.objects.all().order_by('-created_at')
    categories = Reference.objects.values_list('category', flat=True).distinct()
    category_filter = request.GET.get('category')
    
    if category_filter:
        references = references.filter(category=category_filter)
    
    context = {
        'references': references,
        'categories': categories,
        'current_category': category_filter,
    }
    return render(request, 'reference/dashboard.html', context)


def reference_detail(request, pk):
    reference = get_object_or_404(Reference, pk=pk)
    return render(request, 'reference/reference_detail.html', {'reference': reference})
