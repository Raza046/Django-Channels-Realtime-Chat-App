# Generated by Django 3.2.4 on 2023-01-23 08:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0003_auto_20230112_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='Message_receiver', to='auth.user'),
            preserve_default=False,
        ),
    ]
