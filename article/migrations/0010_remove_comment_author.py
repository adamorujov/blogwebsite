# Generated by Django 3.1.5 on 2022-02-10 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0009_auto_20220210_1850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
    ]
