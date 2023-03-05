# Generated by Django 4.1.7 on 2023-02-24 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0031_alter_messageroom_second_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messageroom',
            name='second_user',
        ),
        migrations.AddField(
            model_name='messageroom',
            name='second_user',
            field=models.ManyToManyField(blank=True, null=True, related_name='second_user', to='chat.userprofile'),
        ),
    ]