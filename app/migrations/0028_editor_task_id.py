# Generated by Django 4.2.1 on 2023-08-27 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0027_bgm_upload"),
    ]

    operations = [
        migrations.AddField(
            model_name="editor",
            name="task_id",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="タスクID"
            ),
        ),
    ]
