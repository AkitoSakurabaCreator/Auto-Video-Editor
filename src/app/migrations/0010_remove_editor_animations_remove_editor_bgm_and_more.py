# Generated by Django 4.1.3 on 2023-08-08 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0009_animations_bgm_filters_format'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editor',
            name='animations',
        ),
        migrations.RemoveField(
            model_name='editor',
            name='bgm',
        ),
        migrations.RemoveField(
            model_name='editor',
            name='cut',
        ),
        migrations.RemoveField(
            model_name='editor',
            name='filter_effect',
        ),
        migrations.RemoveField(
            model_name='editor',
            name='movie_format',
        ),
        migrations.RemoveField(
            model_name='editor',
            name='title',
        ),
        migrations.RemoveField(
            model_name='editor',
            name='voice',
        ),
        migrations.RemoveField(
            model_name='editor',
            name='volume',
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='無題のタイトル', max_length=200, verbose_name='動画のタイトル')),
                ('movie_format', models.IntegerField(default=-1, verbose_name='フォーマット')),
                ('voice', models.IntegerField(default=-1, verbose_name='音声')),
                ('filter_effect', models.IntegerField(default=-1, verbose_name='フィルター')),
                ('animations', models.IntegerField(default=-1, verbose_name='アニメーション')),
                ('bgm', models.IntegerField(default=-1, verbose_name='BGM')),
                ('volume', models.IntegerField(default=-1, verbose_name='音声調整')),
                ('cut', models.IntegerField(default=-1, verbose_name='カット')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='editor',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.template'),
        ),
    ]