from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from .services import can_add_task_to_sprint

class SprintTaskMixin:
    """
    Mixin to check if a task can be added to a sprint based on the sprint's task range.
    """

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object() if hasattr(self, "get_object") else None # Assuming get_object() retrieves the task instance
        sprint_id = request.POST.get("sprint") # Assuming sprint ID is sent in POST data
        
        if sprint_id:
            # If a task exists (for UpdateView) or is about to be created (for CreateView)
            if task or request.method == "POST":
                if not can_add_task_to_sprint(task, sprint_id):
                    return HttpResponseBadRequest("Task's creation date is outside the date range of the associated sprint.")
        return super().dispatch(request, *args, **kwargs)