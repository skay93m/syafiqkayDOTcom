from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Task

class TaskListView(ListView):
    model = Task
    template_name = 'taskmanager/task_list.html'
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'taskmanager/task_detail.html'
    context_object_name = 'task'

class TaskCreateView(CreateView):
    model = Task
    template_name = 'taskmanager/task_form.html'
    fields = ['title', 'description', 'status', 'due_date', 'owner', 'epic',]
    
    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.id})

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'taskmanager/task_form.html'
    fields = ['title', 'description', 'status', 'due_date', 'owner', 'epic']

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.id})

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'taskmanager/task_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('task-list')

class HomeView(TemplateView):
    template_name = 'taskmanager/taskmanager.html'

class HelpView(TemplateView):
    template_name = 'taskmanager/help.html'