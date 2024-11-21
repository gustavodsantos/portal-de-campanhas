from django.core.validators import RegexValidator
from django.db import models
from django_min_custom_user.models import MinAbstractUser


class User(MinAbstractUser):
    """Modelo de usuário customizado para autenticação"""

    pass


class Desafio(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome do Desafio')
    descricao = models.TextField(verbose_name='Descrição')
    banner = models.ImageField(upload_to='public/base/imagens', verbose_name='Banner')
    regras_pontuacao = models.TextField(verbose_name='Regras de Pontuação')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return f'{self.nome} ({self.id})'

    class Meta:
        verbose_name = 'Desafio'
        verbose_name_plural = 'Desafios'
        ordering = ['-created_at']


class Corretor(models.Model):
    """Modelo que estende as informações do usuário para corretores"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='corretor', null=True, blank=True, verbose_name='Usuário'
    )
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(r'^\d{11}$', 'Digite um CPF válido com 11 dígitos.')],
        verbose_name='CPF',
    )
    desafios = models.ManyToManyField(Desafio, through='ParticipacaoDesafio', verbose_name='Desafios Participados')

    def __str__(self):
        if self.user:
            return self.user.email
        return f'Corretor sem usuário associado (CPF: {self.cpf})'

    class Meta:
        verbose_name = 'Corretor'
        verbose_name_plural = 'Corretores'


class ParticipacaoDesafio(models.Model):
    """Modelo intermediário para representar a participação de corretores em desafios"""

    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE, verbose_name='Corretor')
    desafio = models.ForeignKey(Desafio, on_delete=models.CASCADE, verbose_name='Desafio')
    aceito = models.BooleanField(default=False, verbose_name='Aceito')
    pontuacao = models.IntegerField(default=0, verbose_name='Pontuação')
    posicao = models.IntegerField(null=True, blank=True, verbose_name='Posição')

    def __str__(self):
        status = 'Aceito' if self.aceito else 'Não Aceito'
        return f'{self.corretor} - {self.desafio} ({status})'

    class Meta:
        verbose_name = 'Participação no Desafio'
        verbose_name_plural = 'Participações nos Desafios'
        ordering = ['-pontuacao', 'posicao']
