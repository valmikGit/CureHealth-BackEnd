# Generated by Django 4.2.6 on 2023-10-27 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_rename_room_name_roommember_room_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roommember',
            name='user',
        ),
    ]