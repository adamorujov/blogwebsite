# Generated by Django 3.1.5 on 2022-02-22 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_newsletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='update_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
