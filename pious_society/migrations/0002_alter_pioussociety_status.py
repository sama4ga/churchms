# Generated by Django 4.2.7 on 2023-11-28 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pious_society', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pioussociety',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Suspended', 'Suspended'), ('Domiciled', 'Domiciled')], default='Active', max_length=10),
        ),
    ]
