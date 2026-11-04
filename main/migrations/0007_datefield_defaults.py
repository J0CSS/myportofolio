import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_experience_starred_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="experience",
            name="started_at",
            field=models.DateField(default=django.utils.timezone.localdate),
        ),
        migrations.AlterField(
            model_name="project",
            name="started_at",
            field=models.DateField(default=django.utils.timezone.localdate),
        ),
        migrations.AlterField(
            model_name="skill",
            name="started_at",
            field=models.DateField(blank=True, default=django.utils.timezone.localdate, null=True),
        ),
    ]
