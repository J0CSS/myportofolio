from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Joshua Carnsyn.S.S",
        "npm": "2506593821",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS student at Universitas Indonesia."
            "A machine learning enthusiast and calculus enjoyer"
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Joshua Carnsyn.S.S",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)