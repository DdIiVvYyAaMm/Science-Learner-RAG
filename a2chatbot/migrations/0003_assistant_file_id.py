# Generated by Django 4.2.16 on 2024-11-01 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a2chatbot', '0002_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='assistant',
            name='file_id',
            field=models.TextField(default='0', verbose_name='File ID'),
        ),
    ]