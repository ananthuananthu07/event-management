# Generated by Django 5.0.3 on 2024-05-02 03:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0029_delete_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(choices=[('debit_card', 'Debit Card'), ('net_banking', 'Net Banking')], max_length=20)),
                ('card_holder_name', models.CharField(blank=True, max_length=100, null=True)),
                ('card_number', models.CharField(blank=True, max_length=16, null=True)),
                ('cvv_number', models.CharField(blank=True, max_length=3, null=True)),
                ('expiry_date', models.CharField(blank=True, max_length=5, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('account_number', models.CharField(blank=True, max_length=14, null=True)),
                ('ifsc_code', models.CharField(blank=True, max_length=15, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=100, max_digits=10)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=15, null=True)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='event_app.booking')),
            ],
        ),
    ]
