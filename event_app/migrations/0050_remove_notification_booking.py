# Generated by Django 5.0.3 on 2024-05-05 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0049_notification_booking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='booking',
        ),
    ]