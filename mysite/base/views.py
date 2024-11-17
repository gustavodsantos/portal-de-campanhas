from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegistroUsuarioForm
from .models import Desafio, ParticipacaoDesafio


def home(request):
    return render(request, 'base/home.html')


def logged_out(request):
    return render(request, 'registration/logged_out.html')


def registrar_usuario(request):
    """View para registrar novos usuários"""
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Faz login automático após o registro
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('base:home')
        else:
            messages.error(request, 'Erro ao realizar o cadastro. Verifique os dados fornecidos.')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registration/registrar_usuario.html', {'form': form})


def listar_desafios(request):
    desafios = Desafio.objects.all()
    return render(request, 'base/listar_desafios.html', {'desafios': desafios})


@login_required
def detalhes_desafio(request, id):
    desafio = get_object_or_404(Desafio, id=id)
    participacao = (
        ParticipacaoDesafio.objects.filter(corretor__user=request.user, desafio=desafio).first()
        if hasattr(request.user, 'corretor') else None
    )
    return render(request, 'base/detalhes_desafio.html', {'desafio': desafio, 'participacao': participacao})


@login_required
def aceitar_desafio(request, id):
    desafio = get_object_or_404(Desafio, id=id)

    if not hasattr(request.user, 'corretor'):
        messages.error(request, 'Você precisa ser um corretor para aceitar desafios.')
        return redirect('base:listar_desafios')

    corretor = request.user.corretor
    participacao, created = ParticipacaoDesafio.objects.get_or_create(corretor=corretor, desafio=desafio)
    participacao.aceito = True
    participacao.save()

    messages.success(request, 'Desafio aceito com sucesso!')
    return redirect('base:listar_desafios')


@login_required
def visualizar_desafios_atribuidos(request):
    participacoes = ParticipacaoDesafio.objects.filter(corretor__user=request.user) \
        if hasattr(request.user, 'corretor') else []
    return render(request, 'base/visualizar_desafios_atribuidos.html', {'participacoes': participacoes})
