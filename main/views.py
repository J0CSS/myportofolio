from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Project, Skill
from main.forms import ProjectForm

def show_main(request):
    context = {
        "name": "Joshua Carnsyn.S.S",
        "npm": "2506593821",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS student at Universitas Indonesia."
            "A machine learning enthusiast and calculus enjoyer"
        ),
        "skills": Skill.objects.all(),
        "projects": Project.objects.prefetch_related("tech_tags").order_by("-started_at")[:3],
        "recent_experience": Experience.objects.all().order_by("-started_at")[:2],
    }
    return render(request, "index.html", context)

def show_experience(request):
    context = {
        "name": "Joshua Carnsyn.S.S",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_projects(request):
    json_response = get_projects_json(request)

    deserialized_data = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [item.object for item in deserialized_data]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Joshua Carnsyn.S.S",
        "projects": projects,
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")