from django.contrib import admin
from django_min_custom_user.admin import MinUserAdmin

from mysite.base.models import Corretor, Desafio, ParticipacaoDesafio, User


@admin.register(User)
class UserAdmin(MinUserAdmin):
    pass


@admin.register(Desafio)
class DesafioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'regras_pontuacao', 'created_at', 'updated_at')


@admin.register(Corretor)
class CorretorAdmin(admin.ModelAdmin):
    list_display = ('user', 'cpf')


@admin.register(ParticipacaoDesafio)
class ParticipacaoDesafioAdmin(admin.ModelAdmin):
    list_display = ('corretor', 'desafio')
