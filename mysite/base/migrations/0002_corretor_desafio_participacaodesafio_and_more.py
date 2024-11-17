# Generated by Django 5.1.3 on 2024-11-15 22:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corretor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=64)),
                ('cpf', models.CharField(max_length=11, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Desafio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('descricao', models.TextField()),
                ('banner', models.ImageField(upload_to='mysite/base/static/base/images/')),
                ('regras_pontuacao', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParticipacaoDesafio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aceito', models.BooleanField(default=False)),
                ('pontuacao', models.IntegerField(default=0)),
                ('posicao', models.IntegerField(blank=True, null=True)),
                ('corretor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.corretor')),
                ('desafio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.desafio')),
            ],
        ),
        migrations.AddField(
            model_name='corretor',
            name='desafios',
            field=models.ManyToManyField(through='base.ParticipacaoDesafio', to='base.desafio'),
        ),
    ]