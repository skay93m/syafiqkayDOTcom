from django.contrib import admin


from .models import Rirekisho, WorkExperience, Education

class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 1

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

@admin.register(Rirekisho)
class RirekishoAdmin(admin.ModelAdmin):
    list_display = ("version", "created_at")
    inlines = [WorkExperienceInline, EducationInline]

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "start_date", "end_date", "rirekisho")
    list_filter = ("company", "start_date")
    search_fields = ("role", "company")

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "field_of_study", "start_date", "end_date", "rirekisho")
    list_filter = ("institution", "start_date")
    search_fields = ("degree", "institution", "field_of_study")
