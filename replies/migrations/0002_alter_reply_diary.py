# Generated by Django 5.1.5 on 2025-02-06 16:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaries', '0002_personality_remove_like_friend_remove_comment_friend_and_more'),
        ('replies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='diary',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='diaries.diary'),
        ),
    ]
