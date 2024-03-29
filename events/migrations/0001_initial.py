# Generated by Django 5.0 on 2023-12-07 14:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='App User First Name')),
                ('last_name', models.CharField(max_length=255, verbose_name='App User Last Name')),
                ('email', models.URLField(verbose_name='App User Email')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Location Name')),
                ('address', models.CharField(max_length=255, verbose_name='Location Address')),
                ('zip_code', models.CharField(max_length=20, verbose_name='Location Zip Code')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Location Phone Number')),
                ('website', models.URLField(max_length=255, verbose_name='Location Website')),
                ('email', models.URLField(verbose_name='Location Email')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Event Name')),
                ('event_date', models.DateField(verbose_name='Event Date')),
                ('manager', models.CharField(max_length=255, verbose_name='Event Manager')),
                ('description', models.TextField(blank=True, null=True, verbose_name=' Event Description')),
                ('attendees', models.ManyToManyField(to='events.appuser')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.location')),
            ],
        ),
    ]
