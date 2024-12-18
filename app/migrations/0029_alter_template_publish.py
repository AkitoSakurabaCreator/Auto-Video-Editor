# Generated by Django 4.2.1 on 2023-08-30 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0028_editor_task_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="template",
            name="publish",
            field=models.CharField(
                choices=[("publish", "公開"), ("limited", "限定公開"), ("close", "非公開")],
                default="非公開",
                max_length=20,
            ),
        ),
    ]
