# taskmanager/views.py

from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from syafiqkaydotcom.decorators import ensure_200_status
from .models import Task, Sprint, Epic

# homepage and help page

@method_decorator(ensure_200_status, name='get')
class ViewTaskManagerHomepage(TemplateView):
    template_name = 'home_and_help/task_manager_homepage.html'

@method_decorator(ensure_200_status, name='get')
class ViewTaskManagerHelpPage(TemplateView):
    template_name = 'home_and_help/task_manager_help_page.html'

# task pages
@method_decorator(ensure_200_status, name='get')
class ViewTaskList(ListView):
    model = Task
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'
    
@method_decorator(ensure_200_status, name='get') 
class ViewTaskCreate(CreateView):
    model = Task
    template_name = 'task/task_form.html'
    fields = '__all__'
    def get_success_url(self):
        return reverse('taskmanager:task-detail', kwargs={'pk': self.object.pk})
    
@method_decorator(ensure_200_status, name='get') 
class ViewTaskDetail(DetailView):
    template_name = "task/task_detail.html"
    model = Task
    context_object_name = 'task'
    
    def get_success_url(self):
        return reverse_lazy('taskmanager:task-detail', kwargs={'pk': self.object.id})

@method_decorator(ensure_200_status, name='get') 
class ViewTaskDelete(DeleteView):
    template_name = "task/task_confirm_delete.html"
    model = Task
    success_url = reverse_lazy('taskmanager:task-list')
    
@method_decorator(ensure_200_status, name='get')
class ViewTaskUpdate(UpdateView):
    model = Task
    template_name = 'task/task_form.html'
    fields = ['title', 'description', 'status', 'due_date', 'owner', 'epic']
    
    def get_success_url(self):
        return reverse_lazy('taskmanager:task-detail', kwargs={'pk': self.object.id})
    
@method_decorator(ensure_200_status, name='get')
class ViewSprintList(ListView):
    model = Sprint
    template_name = 'sprint/sprint_list.html'
    context_object_name = 'sprints'

@method_decorator(ensure_200_status, name='get')
class ViewSprintDetail(DetailView):
    template_name = "sprint/sprint_detail.html"
    model = Sprint
    context_object_name = 'sprint'
    
    def get_success_url(self):
        return reverse_lazy('taskmanager:sprint-detail', kwargs={'pk': self.object.id})

@method_decorator(ensure_200_status, name='get')
class ViewSprintCreate(CreateView):
    model = Sprint
    template_name = 'sprint/sprint_form.html'
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('taskmanager:sprint-detail', kwargs={'pk': self.object.pk})