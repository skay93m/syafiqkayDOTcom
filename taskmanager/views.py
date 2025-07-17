# taskmanager/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Task
from .mixins import SprintTaskMixin
from django.http import Http404, HttpRequest, HttpResponseRedirect, HttpResponse, JsonResponse, Http500
from .services import create_task_and_add_to_sprint, claim_task
from rest_framework import status

class TaskListView(ListView):
    model = Task
    template_name = 'taskmanager/task_list.html'
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'taskmanager/task_detail.html'
    context_object_name = 'task'

class TaskCreateView(SprintTaskMixin, CreateView):
    model = Task
    template_name = 'taskmanager/task_form.html'
    fields = ['title', 'description', 'status', 'due_date', 'owner', 'epic',]
    
    def get_success_url(self):
        return reverse_lazy('taskmanager:task-detail', kwargs={'pk': self.object.id})

class TaskUpdateView(SprintTaskMixin, UpdateView):
    model = Task
    template_name = 'taskmanager/task_form.html'
    fields = ['title', 'description', 'status', 'due_date', 'owner', 'epic']

    def get_success_url(self):
        return reverse_lazy('taskmanager:task-detail', kwargs={'pk': self.object.id})

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'taskmanager/task_confirm_delete.html'
    success_url = reverse_lazy('taskmanager:task-list')

def create_task_on_sprint(request: HttpRequest, sprint_id: int) -> HttpResponseRedirect:
    if request.method == 'POST':
        task_data: dict[str, str] = {
            'title': request.POST.get('title', ''),
            'description': request.POST.get('description', ''),
            'status': request.POST.get('status', 'UNASSIGNED'),
        }
        task = create_task_and_add_to_sprint(task_data, sprint_id, request.user)
        return redirect('taskmanager:task-detail', pk=task.id)
    raise Http404("Not found")

def claim_task_view(request, task_id):
    user_id = request.user.id
    try:
        claim_task(user_id, task_id)
        return JsonResponse({'message': 'Task claimed successfully'})
    except Task.DoesNotExist:
        return HttpResponse("Task does not exist", status=status.HTTP_404_NOT_FOUND)
    except TaskAlreadyClaimedException:
        return HttpResponse("Task already claimed or completed", status=status.HTTP_400_BAD_REQUEST)

def custom_404(request, exception):
    return render(request, '404.html', {}, status=404)

def custom_500(request, exception):
    return render(request, '500.html', {}, status=500)