# Generated by Django 5.0.3 on 2024-05-10 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0057_delete_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
