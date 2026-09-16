from django.forms import ModelForm, TextInput, Textarea, URLInput, DateInput, SelectMultiple, CheckboxSelectMultiple
from main.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "project_tags",
            "tech_tags",
            "project_url",
            "project_image_url",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "project_tags": "Bidang Proyek",
            "tech_tags": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
            "started_at": "Tanggal Proyek Dimulai",
            "ended_at": "Tanggal Proyek Berakhir",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "project_tags": SelectMultiple(
                attrs={ "class": "form-select",}
            ),
            "tech_tags": CheckboxSelectMultiple(),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/username/project",
                }
            ),
            "started_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...",
                }
            ),
        }