# Generated by Django 5.0 on 2023-12-08 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_event_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(verbose_name='Event Date'),
        ),
    ]
