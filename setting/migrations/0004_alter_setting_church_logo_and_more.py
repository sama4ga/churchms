# Generated by Django 5.0.1 on 2024-01-17 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0003_setting_baptism_reg_no_length_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='church_logo',
            field=models.ImageField(default='church_default.jfif', upload_to='church'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='church_saint_logo',
            field=models.ImageField(default='church_default.jfif', upload_to='church'),
        ),
    ]
