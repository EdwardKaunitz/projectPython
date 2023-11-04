# Generated by Django 4.2.5 on 2023-11-04 17:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('painters', '0003_raiting_message_user_painter_user_painter_raiting'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-created', '-updated']},
        ),
        migrations.AlterModelOptions(
            name='painter',
            options={'ordering': ['-created', '-updated']},
        ),
        migrations.AddField(
            model_name='painter',
            name='participants',
            field=models.ManyToManyField(related_name='participants', to=settings.AUTH_USER_MODEL),
        ),
    ]