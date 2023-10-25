# Generated by Django 4.2.6 on 2023-10-25 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='firstname',
            field=models.CharField(default='first name not mentioned', max_length=30),
        ),
        migrations.AddField(
            model_name='newuser',
            name='lastname',
            field=models.CharField(default='last name not mentioned', max_length=150),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]