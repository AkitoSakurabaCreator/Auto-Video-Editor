# Generated by Django 4.2.1 on 2023-08-24 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0018_editor_edited"),
    ]

    operations = [
        migrations.AlterField(
            model_name="editor",
            name="edited",
            field=models.CharField(max_length=250, verbose_name="編集済みファイル"),
        ),
    ]
