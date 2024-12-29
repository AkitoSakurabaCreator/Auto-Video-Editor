# Generated by Django 4.2.1 on 2023-08-30 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0030_alter_template_animations_alter_template_bgm_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Model",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("modelId", models.CharField(max_length=10, verbose_name="モデル")),
                ("title", models.CharField(max_length=200, verbose_name="タイトル")),
            ],
            options={
                "verbose_name": "音声認識一覧",
                "verbose_name_plural": "音声認識一覧",
            },
        ),
        migrations.CreateModel(
            name="Publish",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("publishName", models.CharField(max_length=10, verbose_name="位置")),
                ("title", models.CharField(max_length=200, verbose_name="タイトル")),
            ],
            options={
                "verbose_name": "公開範囲一覧",
                "verbose_name_plural": "公開範囲一覧",
            },
        ),
        migrations.CreateModel(
            name="Telop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("telopName", models.CharField(max_length=10, verbose_name="位置")),
                ("title", models.CharField(max_length=200, verbose_name="タイトル")),
            ],
            options={
                "verbose_name": "テロップ一覧",
                "verbose_name_plural": "テロップ一覧",
            },
        ),
    ]