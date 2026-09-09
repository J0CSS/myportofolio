import re
import uuid
from django.db import models
from django.utils import timezone

# TAGS
class ProjectTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Project Tags"

    def __str__(self):
        return self.name


class TechTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Tech Tags"

    def __str__(self):
        return self.name


class SkillTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Skill Tags"

    def __str__(self):
        return self.name


# MAIN MODELS
class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateField(default=timezone.now)
    ended_at = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None


class Project(models.Model):    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()

    project_tags = models.ManyToManyField(ProjectTag, blank=True)
    tech_tags = models.ManyToManyField(TechTag, blank=True)

    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateField(default=timezone.now)
    ended_at = models.DateField(blank=True, null=True)

    is_featured = models.BooleanField(
        default=False, 
        help_text="Check this box to display this project on the homepage preview."
    )
    
    # Optional: Short summary field, custom project summary for homepage
    summary = models.CharField(
        max_length=300, 
        blank=True, 
        help_text="Brief snippet for homepage card. If left blank, description will be truncated."
    )

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

    @property
    def primary_tag(self):
        first_tag = self.project_tags.first()
        return first_tag.name if first_tag else "General"

    @property
    def display_summary(self):
        # use summary if filled out manually
        if self.summary.strip():
            return self.summary
            
        # Extract first sentence from description
        if self.description:
            # Splits at '.', '!', or '?' followed by a space
            sentences = re.split(r'(?<=[.!?])\s+', self.description)
            return sentences[0]
            
        return ""


class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    
    # Made optional so you don't have to fill it in for every skill
    description = models.TextField(blank=True)

    # Plural naming convention for ManyToMany relations
    category = models.ManyToManyField(SkillTag, blank=True)
    
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateField(default=timezone.now, blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, default="⚡", help_text="Emoji or icon identifier")

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    @property
    def name(self):
        return self.title

    @property
    def category_display(self):
        tags = self.category.all()
        return ", ".join([tag.name for tag in tags]) if tags else "General"

    @property
    def years_of_experience(self):
        """Calculates years of experience dynamically from started_at."""
        if self.started_at:
            from django.utils import timezone
            today = timezone.now().date()
            return max(0, today.year - self.started_at.year)
        return 0