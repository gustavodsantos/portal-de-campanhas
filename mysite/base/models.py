from django.db import models
from django_min_custom_user.models import MinAbstractUser


class User(MinAbstractUser):
    """Modelo de usuário customizado para autenticação"""

    pass


class Desafio(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    banner = models.ImageField(upload_to='mysite/base/static/base/images/')
    regras_pontuacao = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Corretor(models.Model):
    """Modelo que estende as informações do usuário para corretores"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='corretor', null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True)
    desafios = models.ManyToManyField(Desafio, through='ParticipacaoDesafio')

    def __str__(self):
        return self.user.email if self.user else self.cpf  # Retorna o email como identificação


class ParticipacaoDesafio(models.Model):
    """Modelo intermediário para representar a participação de corretores em desafios"""

    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE)
    desafio = models.ForeignKey(Desafio, on_delete=models.CASCADE)
    aceito = models.BooleanField(default=False)
    pontuacao = models.IntegerField(default=0)
    posicao = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.corretor} - {self.desafio}'
