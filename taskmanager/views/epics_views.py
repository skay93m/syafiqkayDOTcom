# taskmanager/views/epic_views.py

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