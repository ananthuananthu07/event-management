# Generated by Django 5.0.3 on 2024-05-01 07:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0026_delete_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100, null=True)),
                ('customer_number', models.CharField(max_length=15, null=True)),
                ('customer_email', models.EmailField(max_length=254)),
                ('district', models.CharField(max_length=100, null=True)),
                ('location', models.CharField(max_length=200, null=True)),
                ('landmark', models.CharField(max_length=200, null=True)),
                ('date', models.DateField()),
                ('duration', models.PositiveIntegerField(max_length=10, null=True)),
                ('food_type', models.CharField(choices=[('Boffey', 'Boffey'), ('A la carte', 'A la carte'), ('Default', 'Default')], max_length=20)),
                ('dj_party_needed', models.BooleanField(default=False)),
                ('comp_cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event_app.companyprofile')),
                ('company_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
