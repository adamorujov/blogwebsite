# Generated by Django 3.1.5 on 2022-02-21 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('conf_num', models.CharField(max_length=15)),
                ('confirmed', models.BooleanField(default=False)),
            ],
        ),
    ]
