from django.urls import path
from . import views

app_name = "noto_garden"

urlpatterns = [
    path("", views.garden_dashboard, name="dashboard"),
    path("guide/", views.guide_view, name="guide"),
    path("note/<str:unique_id>/", views.note_detail, name="note_detail"),
    path("create/", views.note_create, name="note_create"),
    path("edit/<str:unique_id>/", views.note_edit, name="note_edit"),
    path("graph/", views.graph_view, name="graph"),
    path("search/", views.search_notes, name="search_notes"),
    path("coming-soon/", views.coming_soon, name="coming_soon"),
]