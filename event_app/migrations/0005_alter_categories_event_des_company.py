# Generated by Django 5.0.3 on 2024-03-29 06:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0004_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='event_des',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comp_name', models.CharField(max_length=100, null=True)),
                ('comp_location', models.CharField(max_length=200, null=True)),
                ('comp_image', models.ImageField(null=True, upload_to='comp_images')),
                ('comp_prize', models.IntegerField(null=True)),
                ('comp_event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cat', to='event_app.categories')),
                ('comp_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type', to='event_app.eventsclass')),
            ],
        ),
    ]