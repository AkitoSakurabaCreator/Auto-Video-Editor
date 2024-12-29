# Generated by Django 4.1.3 on 2023-08-08 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_section_banner_alter_section_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='プランレベル')),
                ('content', models.TextField(verbose_name='内容')),
            ],
            options={
                'verbose_name': 'プラン一覧',
                'verbose_name_plural': 'プラン一覧',
            },
        ),
    ]
