# taskmanager/views/sprints_views.py

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
