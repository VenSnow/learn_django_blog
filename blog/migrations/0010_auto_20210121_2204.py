# Generated by Django 3.1.5 on 2021-01-21 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20210121_2157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='status',
        ),
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Активный'),
        ),
    ]