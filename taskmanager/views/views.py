# taskmanager/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Task
from .views.mixins import SprintTaskMixin

# Task Views
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
    fields = ['title', 'description', 'status', 'due_date', 'owner', 'epic']
    
    def get_success_url(self):
        return reverse_lazy('taskmanager:task-detail', kwargs={'pk': self.object.id})
class TaskUpdateView(SprintTaskMixin, UpdateView):
    model = Task
    template_name = 'taskmanager/task_form.html'
    fields = ['title', 'description', 'status', 'due_date', 'owner', 'epic',]

    def get_success_url(self):
        return reverse_lazy('taskmanager:task-detail', kwargs={'pk': self.object.id})
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'taskmanager/task_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('taskmanager:task-list')

# Sprint Views
class SprintCreateView(CreateView):
    model = Sprint
    fields = ['name', 'description', 'start_date', 'end_date', 'created_by']

    def get_success_url(self):
        return reverse_lazy('taskmanager:sprint-detail', kwargs={'pk': self.object.id})
class SprintUpdateView(UpdateView):
    model = Sprint
    fields = ['name', 'description', 'start_date', 'end_date', 'created_by']

    def get_success_url(self):
        return reverse_lazy('taskmanager:sprint-detail', kwargs={'pk': self.object.id})

class SprintDeleteView(DeleteView):
    model = Sprint

    def get_success_url(self):
        return reverse_lazy('taskmanager:sprint-list')

# Epic Views
class EpicCreateView(CreateView):
    model = Epic
    fields = ['name', 'description', 'created_by']

    def get_success_url(self):
        return reverse_lazy('taskmanager:epic-detail', kwargs={'pk': self.object.id})

class EpicUpdateView(UpdateView):
    model = Epic
    fields = ['name', 'description', 'created_by']

    def get_success_url(self):
        return reverse_lazy('taskmanager:epic-detail', kwargs={'pk': self.object.id})

class EpicDeleteView(DeleteView):
    model = Epic

    def get_success_url(self):
        return reverse_lazy('taskmanager:epic-list')