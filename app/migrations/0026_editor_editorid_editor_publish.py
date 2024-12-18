# Generated by Django 4.2.1 on 2023-08-27 05:41

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0025_template_publish_template_templateid"),
    ]

    operations = [
        migrations.AddField(
            model_name="editor",
            name="editorId",
            field=models.SlugField(
                default=app.models.create_id,
                max_length=30,
                unique=True,
                verbose_name="EditorID",
            ),
        ),
        migrations.AddField(
            model_name="editor",
            name="publish",
            field=models.BooleanField(default=False),
        ),
    ]
