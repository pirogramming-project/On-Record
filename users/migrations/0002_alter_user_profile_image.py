# Generated by Django 5.1.5 on 2025-02-08 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='images/base-user-image.png', null=True, upload_to='profile_images/%Y%m%d'),
        ),
    ]
