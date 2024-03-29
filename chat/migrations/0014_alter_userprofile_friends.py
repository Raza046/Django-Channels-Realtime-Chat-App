# Generated by Django 4.1.7 on 2023-02-15 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_friendrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='user_friends', to='chat.userprofile'),
        ),
    ]
