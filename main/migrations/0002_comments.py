# Generated by Django 5.0.3 on 2024-04-23 13:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('comment', models.TextField()),
                ('dateTime', models.DateField(verbose_name=datetime.date.today)),
                ('isActive', models.BooleanField()),
            ],
        ),
    ]
