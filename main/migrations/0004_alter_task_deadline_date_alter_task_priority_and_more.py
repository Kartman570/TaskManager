# Generated by Django 4.2.3 on 2023-08-15 03:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0003_tag_task"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="deadline_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="task",
            name="tags",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tag",
                to="main.tag",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="worker",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="worker",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
