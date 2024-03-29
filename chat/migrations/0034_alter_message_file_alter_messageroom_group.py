# Generated by Django 4.1.5 on 2023-03-14 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0033_remove_message_receiver_remove_message_seen_by_users_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='static'),
        ),
        migrations.AlterField(
            model_name='messageroom',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_groups', to='chat.messagegroup'),
        ),
    ]
