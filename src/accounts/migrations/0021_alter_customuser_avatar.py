# Generated by Django 4.1.3 on 2023-02-28 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_alter_customuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, default='Users/default.jpg', null=True, upload_to='Users/ProfileImages', verbose_name='プロフィール画像'),
        ),
    ]