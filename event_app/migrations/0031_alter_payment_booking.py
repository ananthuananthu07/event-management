# Generated by Django 5.0.3 on 2024-05-02 10:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0030_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_app.booking'),
        ),
    ]