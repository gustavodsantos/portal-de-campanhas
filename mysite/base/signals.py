from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Corretor, User


@receiver(post_save, sender=User)
def criar_corretor(sender, instance, created, **kwargs):
    """
    Cria automaticamente um registro em Corretor sempre que um User for criado.
    """
    if created:
        Corretor.objects.create(user=instance)
        print(f'Corretor criado para o usuário {instance.email}')
