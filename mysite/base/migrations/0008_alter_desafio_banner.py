# Generated by Django 5.1.3 on 2024-11-19 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_desafio_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='desafio',
            name='banner',
            field=models.ImageField(upload_to='public/img/', verbose_name='Banner'),
        ),
    ]
