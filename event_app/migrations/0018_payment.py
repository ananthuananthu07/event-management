# Generated by Django 5.0.3 on 2024-04-17 13:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0017_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('payment_method', models.CharField(choices=[('option1', 'Credit or Debit card'), ('option2', 'Paytm')], default='option1', max_length=50)),
                ('card_number', models.CharField(blank=True, max_length=16, null=True)),
                ('name_on_card', models.CharField(blank=True, max_length=200, null=True)),
                ('cvv_number', models.CharField(blank=True, max_length=3, null=True)),
                ('expiry_date', models.CharField(blank=True, max_length=5, null=True)),
                ('transaction_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('payment_time', models.TimeField(blank=True, null=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='event_app.appointment')),
            ],
        ),
    ]
