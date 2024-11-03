# Generated by Django 4.2.16 on 2024-11-01 01:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assistant',
            fields=[
                ('assistant_id', models.TextField(verbose_name='Assistant ID')),
                ('video_name', models.CharField(default='', max_length=100, verbose_name='videoname')),
                ('vector_store_id', models.TextField(verbose_name='Vector store ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
