# Generated by Django 5.0 on 2023-12-29 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_notificaton_receiver_alter_chat_sender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='sender',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
