# Generated by Django 5.0 on 2023-12-17 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_event_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='owner',
            field=models.IntegerField(default=1, verbose_name='location owner'),
        ),
    ]
