from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Project, Skill
from main.forms import ProjectForm, ExperienceForm

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

# EXPERIENCES
def show_experiences(request):
    json_response = get_experiences_json(request)

    deserialized_data = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [item.object for item in deserialized_data]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Joshua Carnsyn.S.S",
        "projects": experiences,
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experiences.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experiences")

    context = {
        "name": "Joshua Carnsyn.S.S",
        "form": form,
    }
    return render(request, "experiences_form.html", context)

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    expereiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", expereiences)
    return HttpResponse(experiences_json, content_type="application/json")

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experiences")

    return redirect("main:show_experiences")

def edit_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    
    form = ExperienceForm(request.POST or None, instance=experience)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_experiences')

    context = {
        'form': form,
        'page_title': 'Edit Experience',
        'button_text': 'Simpan Perubahan'
    }

    return render(request, 'experiences_form.html', context)

# PROJECTS
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
        "name": "Joshua Carnsyn.S.S",
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

def edit_project(request, id):
    project = get_object_or_404(Project, pk=id)
    
    form = ProjectForm(request.POST or None, instance=project)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_projects')

    context = {
        'form': form,
        'page_title': 'Edit Project',
        'button_text': 'Simpan Perubahan'
    }

    return render(request, 'projects_form.html', context)