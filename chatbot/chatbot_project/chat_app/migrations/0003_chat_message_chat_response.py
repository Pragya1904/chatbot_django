# Generated by Django 5.0.7 on 2024-07-20 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0002_chat_delete_chatbot'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='message',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='chat',
            name='response',
            field=models.TextField(default=None, null=True),
        ),
    ]
