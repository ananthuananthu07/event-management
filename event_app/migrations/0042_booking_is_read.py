# Generated by Django 5.0.3 on 2024-05-05 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0041_remove_payment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
