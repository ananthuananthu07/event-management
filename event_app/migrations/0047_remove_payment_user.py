# Generated by Django 5.0.3 on 2024-05-05 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0046_alter_payment_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
    ]
