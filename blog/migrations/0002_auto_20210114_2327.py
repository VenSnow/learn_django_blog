# Generated by Django 3.1.5 on 2021-01-14 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-publish',), 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
    ]
