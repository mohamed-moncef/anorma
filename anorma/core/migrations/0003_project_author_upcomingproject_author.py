# Generated by Django 5.1.7 on 2025-03-24 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_project_background_color_project_font_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='author',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='upcomingproject',
            name='author',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
