from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience, Project, Skill


class ProjectSerializer(serializers.ModelSerializer):
    project_tag_names = serializers.SerializerMethodField()
    tech_tag_names = serializers.SerializerMethodField()
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "project_tags", "tech_tags",
            "project_tag_names", "tech_tag_names",
            "project_url", "project_image_url", "started_at", "ended_at",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def get_project_tag_names(self, obj):
        return [tag.name for tag in obj.project_tags.all()]

    def get_tech_tag_names(self, obj):
        return [tag.name for tag in obj.tech_tags.all()]

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class ExperienceSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", "category", "category_display",
            "thumbnail", "started_at", "ended_at", "star_count",
            "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        return bool(request and request.user.is_authenticated and
                    request.user in obj.starred_by.all())

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class SkillSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(read_only=True)
    years_of_experience = serializers.IntegerField(read_only=True)

    class Meta:
        model = Skill
        fields = [
            "id", "title", "description", "category", "category_display",
            "thumbnail", "started_at", "icon", "years_of_experience",
        ]
        read_only_fields = [
            "id", "category_display", "years_of_experience",
        ]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value).strip()

    def validate_icon(self, value):
        return strip_tags(value).strip()
