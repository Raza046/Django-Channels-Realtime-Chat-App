# Generated by Django 3.2.4 on 2023-02-15 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0009_auto_20230208_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagereaction',
            name='reaction',
            field=models.CharField(choices=[('Smile', 'Smile'), ('Funny', 'Funny'), ('Angry', 'Angry'), ('Sad', 'Sad'), ('Crying', 'Crying'), ('Heart', 'Heart')], max_length=100),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prof_image', models.FileField(upload_to='static')),
                ('friends', models.ManyToManyField(to='chat.UserProfile', verbose_name='user_friends')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'UserProfile',
                'verbose_name_plural': 'UserProfiles',
            },
        ),
    ]