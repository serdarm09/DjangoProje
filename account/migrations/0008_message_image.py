# Generated by Django 5.0.4 on 2024-06-10 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, default='', null=True, upload_to='message_image'),
        ),
    ]