# Generated by Django 5.0.3 on 2024-05-10 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0056_messages'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Messages',
        ),
    ]