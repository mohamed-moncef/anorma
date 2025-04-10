# Generated by Django 5.1.7 on 2025-04-06 13:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0006_remove_contentblock_content_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contentblock',
            name='image',
        ),
        migrations.RemoveField(
            model_name='contentblock',
            name='project',
        ),
        migrations.RemoveField(
            model_name='contentblock',
            name='text_content',
        ),
        migrations.RemoveField(
            model_name='contentblock',
            name='video_file',
        ),
        migrations.RemoveField(
            model_name='project',
            name='image',
        ),
        migrations.AddField(
            model_name='contentblock',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='contentblock',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='background_color',
            field=models.CharField(default='#000000', max_length=7),
        ),
        migrations.AlterField(
            model_name='project',
            name='font_color',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
        migrations.AlterField(
            model_name='upcomingproject',
            name='background_color',
            field=models.CharField(default='#000000', max_length=7),
        ),
        migrations.AlterField(
            model_name='upcomingproject',
            name='font_color',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
    ]
