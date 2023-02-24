# Generated by Django 4.1.7 on 2023-02-16 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0018_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notif_from_user', to='chat.userprofile'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notif_to_user', to='chat.userprofile'),
        ),
    ]