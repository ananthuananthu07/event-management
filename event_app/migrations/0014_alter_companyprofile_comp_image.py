# Generated by Django 5.0.3 on 2024-04-08 23:52

import event_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0013_remove_companyprofile_comp_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='comp_image',
            field=models.ImageField(default=event_app.models.default_profile_pic, upload_to='comp_images'),
        ),
    ]
