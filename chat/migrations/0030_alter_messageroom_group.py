# Generated by Django 4.1.7 on 2023-02-23 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0029_remove_messagegroup_group_admin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageroom',
            name='group',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_groups', to='chat.messagegroup'),
        ),
    ]
