# Generated by Django 4.1.3 on 2023-08-08 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_editor_animations_editor_bgm_editor_cut_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Animations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='タイトル')),
                ('content', models.TextField(verbose_name='本文')),
            ],
            options={
                'verbose_name': 'アニメーション一覧',
                'verbose_name_plural': 'アニメーション一覧',
            },
        ),
        migrations.CreateModel(
            name='BGM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='タイトル')),
                ('content', models.TextField(verbose_name='本文')),
            ],
            options={
                'verbose_name': 'BGM一覧',
                'verbose_name_plural': 'BGM一覧',
            },
        ),
        migrations.CreateModel(
            name='Filters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='タイトル')),
                ('content', models.TextField(verbose_name='本文')),
            ],
            options={
                'verbose_name': 'フィルタ一覧',
                'verbose_name_plural': 'フィルタ一覧',
            },
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='タイトル')),
                ('content', models.TextField(verbose_name='本文')),
            ],
            options={
                'verbose_name': 'フォーマット一覧',
                'verbose_name_plural': 'フォーマット一覧',
            },
        ),
    ]
