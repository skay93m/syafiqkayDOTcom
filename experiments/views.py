from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Experiment


def dashboard(request):
    """Dashboard view showing all experiments with pagination."""
    experiments = Experiment.objects.filter(is_published=True)
    
    # Pagination
    paginator = Paginator(experiments, 5)  # 5 experiments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'experiments': page_obj,
        'total_experiments': experiments.count(),
        'page_obj': page_obj,
    }
    return render(request, 'experiments/dashboard.html', context)


def experiment_detail(request, slug):
    """Detail view for a single experiment."""
    experiment = get_object_or_404(Experiment, slug=slug, is_published=True)
    
    context = {
        'experiment': experiment,
    }
    return render(request, 'experiments/experiment_detail.html', context)


def coming_soon(request):
    """Coming soon placeholder view."""
    return render(request, 'experiments/coming_soon.html')
