# Generated by Django 5.0.3 on 2024-05-10 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0054_message_is_unread'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='is_unread',
        ),
    ]
