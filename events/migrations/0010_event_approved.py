# Generated by Django 5.0 on 2023-12-19 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_delete_appuser_alter_event_attendees'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='approved'),
        ),
    ]