# Generated by Django 4.2.1 on 2023-08-24 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0019_alter_editor_edited"),
    ]

    operations = [
        migrations.AlterField(
            model_name="editor",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
