# Generated by Django 3.2.4 on 2021-06-26 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0002_user_roles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='roles',
        ),
        migrations.AddField(
            model_name='user',
            name='resource_access',
            field=models.JSONField(default={}, null=True),
        ),
    ]
