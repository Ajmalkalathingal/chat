# Generated by Django 5.0 on 2023-12-27 08:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_notificaton_user_notificaton_receiver_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificaton',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='notificaton',
            name='sender',
        ),
        migrations.AddField(
            model_name='notificaton',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
