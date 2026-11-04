from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project, TechTag


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experiences")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experiences"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experiences.html")
        self.assertContains(response, reverse("api:experience-list"))
        api_response = self.client.get(reverse("api:experience-list"))
        experience_data = api_response.json()[0]
        self.assertEqual(experience_data["title"], self.experience.title)
        self.assertEqual(experience_data["description"], self.experience.description)
        self.assertEqual(experience_data["category_display"], "Part-Time")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experiences"))

        self.assertContains(response, "Belum ada experience yang ditambahkan atau ditemukan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.localdate()
        self.experience.save()

        self.assertFalse(self.experience.is_ongoing)
        response = self.client.get(reverse("api:experience-list"))
        self.assertEqual(response.json()[0]["ended_at"], timezone.localdate().isoformat())

class ProjectPageTest(TestCase):

    def test_project_page_url_and_template(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_project_data_appears_on_page(self):
        tech = TechTag.objects.create(name="Python")
        project = Project.objects.create(
            title="NLP Text Similarity",
            description="A machine learning project for text similarity comparison.",
        )
        project.tech_tags.add(tech)

        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("api:project-list"))
        api_response = self.client.get(reverse("api:project-list"))
        project_data = api_response.json()[0]
        self.assertEqual(project_data["title"], project.title)
        self.assertEqual(project_data["description"], project.description)
        self.assertEqual(project_data["tech_tag_names"], ["Python"])
        self.assertIsNone(project_data["ended_at"])

    def test_empty_project_message_appears(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Belum ada proyek yang ditambahkan atau ditemukan.")
        api_response = self.client.get(reverse("api:project-list"))
        self.assertEqual(api_response.json(), [])
