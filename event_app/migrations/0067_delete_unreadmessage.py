# Generated by Django 5.0.3 on 2024-05-16 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0066_unreadmessage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UnreadMessage',
        ),
    ]
