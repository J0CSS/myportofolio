from django.contrib import admin
from .models import (
    ProjectTag, TechTag, SkillTag, 
    Experience, Project, Skill
)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'started_at', 'ended_at')
    list_filter = ('is_featured', 'project_tags', 'tech_tags')
    search_fields = ('title', 'description')
    filter_horizontal = ('project_tags', 'tech_tags')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('title', 'started_at', 'years_of_experience')
    filter_horizontal = ('category',)

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'started_at', 'ended_at')
    list_filter = ('category',)

# Register tag models directly
admin.site.register(ProjectTag)
admin.site.register(TechTag)
admin.site.register(SkillTag)