# Generated by Django 4.2.1 on 2023-08-30 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0032_alter_publish_publishname_alter_template_model_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Language",
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
                ("code", models.CharField(max_length=10, verbose_name="言語コード")),
                ("title", models.CharField(max_length=200, verbose_name="タイトル")),
            ],
            options={
                "verbose_name": "言語一覧",
                "verbose_name_plural": "言語一覧",
            },
        ),
        migrations.AlterModelOptions(
            name="model",
            options={"verbose_name": "音声認識モデル一覧", "verbose_name_plural": "音声認識モデル一覧"},
        ),
        migrations.AlterField(
            model_name="template",
            name="language",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app.language",
            ),
        ),
    ]
