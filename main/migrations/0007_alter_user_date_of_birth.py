# Generated by Django 4.2.3 on 2023-08-16 01:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0006_alter_user_is_staff"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
    ]