# Generated by Django 4.2.1 on 2023-08-30 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0034_voice_alter_template_translate_alter_template_voice"),
    ]

    operations = [
        migrations.AlterField(
            model_name="editor",
            name="publish",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app.publish",
            ),
        ),
    ]
