# Generated by Django 5.0.4 on 2024-06-09 21:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='istek',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.bagisistegi'),
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]