# Generated by Django 4.2.3 on 2023-07-15 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_profile_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followers',
            field=models.IntegerField(default=int),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.IntegerField(default=int),
            preserve_default=False,
        ),
    ]
