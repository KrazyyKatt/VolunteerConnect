# Generated by Django 5.1.2 on 2025-02-05 22:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_event_participants_alter_participation_event_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='participants',
        ),
        migrations.AlterField(
            model_name='participation',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='main.event'),
        ),
        migrations.AlterField(
            model_name='participation',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participations', to=settings.AUTH_USER_MODEL),
        ),
    ]
