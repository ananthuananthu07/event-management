# Generated by Django 5.0.3 on 2024-04-03 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0009_remove_companyprofile_comp_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyprofile',
            name='comp_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='comp_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]