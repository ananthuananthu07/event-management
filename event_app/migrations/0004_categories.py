# Generated by Django 5.0.3 on 2024-03-28 06:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0003_remove_eventsclass_mini_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=100, null=True)),
                ('event_des', models.CharField(max_length=200, null=True)),
                ('event_image', models.ImageField(null=True, upload_to='category_images')),
                ('event_prize', models.IntegerField(null=True)),
                ('event_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event', to='event_app.eventsclass')),
            ],
        ),
    ]
