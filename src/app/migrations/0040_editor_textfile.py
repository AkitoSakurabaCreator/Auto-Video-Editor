# Generated by Django 4.2.1 on 2023-08-30 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0039_alter_editor_publish"),
    ]

    operations = [
        migrations.AddField(
            model_name="editor",
            name="textFile",
            field=models.FileField(
                blank=True, null=True, upload_to="", verbose_name="テキストファイル"
            ),
        ),
    ]
