# Generated by Django 4.1.3 on 2023-08-07 05:32

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_editor_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editor',
            name='upload',
            field=models.FileField(blank=True, upload_to=app.models.uploadFile, verbose_name='動画ファイル'),
        ),
    ]
