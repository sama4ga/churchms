# Generated by Django 5.0.1 on 2024-01-12 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('church', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='all_day',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
