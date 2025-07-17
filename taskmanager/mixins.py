from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from .services.services import can_add_task_to_sprint

class SprintTaskMixin:
    """
    Mixin to check if a task can be added to a sprint based on the sprint's task range.
    """

    def dispatch(self, request, *args, **kwargs):
        sprint_id = request.POST.get("sprint") # Assuming sprint ID is sent in POST data
        
        # Only try to get the object if this is an UpdateView (where we have a pk)
        task = None
        if 'pk' in kwargs and hasattr(self, "get_object"):
            task = self.get_object()
        
        if sprint_id:
            # If a task exists (for UpdateView) or is about to be created (for CreateView)
            if task or request.method == "POST":
                if not can_add_task_to_sprint(task, sprint_id):
                    return HttpResponseBadRequest("Task's creation date is outside the date range of the associated sprint.")
        return super().dispatch(request, *args, **kwargs)