# Generated by Django 5.0.1 on 2024-01-16 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parishioner', '0006_alter_layapostolateinfo_lay_apostolate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parishioner',
            name='passport',
            field=models.ImageField(default='user_default.jfif', upload_to='passports'),
        ),
    ]
