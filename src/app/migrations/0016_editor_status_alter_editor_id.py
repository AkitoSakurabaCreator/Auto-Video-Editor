# Generated by Django 4.2.1 on 2023-08-24 02:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0015_plan"),
    ]

    operations = [
        migrations.AlterField(
            model_name="editor",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
