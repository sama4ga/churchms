# Generated by Django 4.2.7 on 2023-11-27 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LayApostolate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slogan', models.CharField(blank=True, max_length=100)),
                ('short_name', models.CharField(blank=True, max_length=10)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Suspended', 'Suspended'), ('Domiciled', 'Domiciled'), ('Deleted', 'Deleted')], default='Active', max_length=10)),
            ],
        ),
    ]
