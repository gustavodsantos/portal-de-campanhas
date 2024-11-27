# Generated by Django 5.1.3 on 2024-11-18 00:09

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_corretor_nome_corretor_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='corretor',
            options={'verbose_name': 'Corretor', 'verbose_name_plural': 'Corretores'},
        ),
        migrations.AlterModelOptions(
            name='desafio',
            options={'ordering': ['-created_at'], 'verbose_name': 'Desafio', 'verbose_name_plural': 'Desafios'},
        ),
        migrations.AlterModelOptions(
            name='participacaodesafio',
            options={'ordering': ['-pontuacao', 'posicao'], 'verbose_name': 'Participação no Desafio', 'verbose_name_plural': 'Participações nos Desafios'},
        ),
        migrations.AlterField(
            model_name='corretor',
            name='cpf',
            field=models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator('^\\d{11}$', 'Digite um CPF válido com 11 dígitos.')], verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='corretor',
            name='desafios',
            field=models.ManyToManyField(through='base.ParticipacaoDesafio', to='base.desafio', verbose_name='Desafios Participados'),
        ),
        migrations.AlterField(
            model_name='corretor',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='corretor', to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AlterField(
            model_name='desafio',
            name='banner',
            field=models.ImageField(upload_to='banners/', verbose_name='Banner'),
        ),
        migrations.AlterField(
            model_name='desafio',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='desafio',
            name='descricao',
            field=models.TextField(verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='desafio',
            name='nome',
            field=models.CharField(max_length=255, verbose_name='Nome do Desafio'),
        ),
        migrations.AlterField(
            model_name='desafio',
            name='regras_pontuacao',
            field=models.TextField(verbose_name='Regras de Pontuação'),
        ),
        migrations.AlterField(
            model_name='desafio',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
        migrations.AlterField(
            model_name='participacaodesafio',
            name='aceito',
            field=models.BooleanField(default=False, verbose_name='Aceito'),
        ),
        migrations.AlterField(
            model_name='participacaodesafio',
            name='corretor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.corretor', verbose_name='Corretor'),
        ),
        migrations.AlterField(
            model_name='participacaodesafio',
            name='desafio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.desafio', verbose_name='Desafio'),
        ),
        migrations.AlterField(
            model_name='participacaodesafio',
            name='pontuacao',
            field=models.IntegerField(default=0, verbose_name='Pontuação'),
        ),
        migrations.AlterField(
            model_name='participacaodesafio',
            name='posicao',
            field=models.IntegerField(blank=True, null=True, verbose_name='Posição'),
        ),
    ]