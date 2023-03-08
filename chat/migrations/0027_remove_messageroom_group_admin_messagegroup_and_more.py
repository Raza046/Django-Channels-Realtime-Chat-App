# Generated by Django 4.1.7 on 2023-02-22 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0026_remove_messageroom_message_group_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messageroom',
            name='group_admin',
        ),
        migrations.CreateModel(
            name='MessageGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('group_image', models.FileField(upload_to='static')),
                ('group_admin', models.ManyToManyField(null=True, related_name='group_admins', to='chat.userprofile')),
            ],
            options={
                'verbose_name': 'MessageGroup',
                'verbose_name_plural': 'MessageGroups',
            },
        ),
        migrations.AddField(
            model_name='messageroom',
            name='group',
            field=models.ManyToManyField(null=True, related_name='message_groups', to='chat.messagegroup'),
        ),
    ]
