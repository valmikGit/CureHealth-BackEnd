# Generated by Django 4.2.6 on 2023-10-24 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoomMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('uid', models.CharField(max_length=200)),
                ('room_Name', models.CharField(max_length=200, verbose_name='Room Name')),
            ],
        ),
    ]