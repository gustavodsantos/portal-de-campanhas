from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AtribuirDesafioForm, CorretorForm, DesafioForm
from .models import Corretor, Desafio, ParticipacaoDesafio


# Decorator para garantir que o usuário tem um perfil de Corretor
def require_corretor(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            request.corretor = Corretor.objects.get(user=request.user)
        except Corretor.DoesNotExist:
            raise PermissionDenied('Você precisa ter um perfil de corretor para acessar esta página.')
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def home(request):
    return render(request, 'base/home.html')


def logged_out(request):
    return render(request, 'registration/logged_out.html')


def listar_desafios(request):
    desafios = Desafio.objects.all()
    return render(request, 'base/listar_desafios.html', {'desafios': desafios})


@login_required
@require_corretor
def detalhes_desafio(request, id):
    desafio = get_object_or_404(Desafio, id=id)
    participacao = ParticipacaoDesafio.objects.filter(corretor=request.corretor, desafio=desafio).first()
    return render(request, 'base/detalhes_desafio.html', {'desafio': desafio, 'participacao': participacao})


@login_required
@require_corretor
def aceitar_desafio(request, id):
    desafio = get_object_or_404(Desafio, id=id)
    participacao, created = ParticipacaoDesafio.objects.get_or_create(corretor=request.corretor, desafio=desafio)
    participacao.aceito = True
    participacao.save()

    messages.success(request, 'Desafio aceito com sucesso!')
    return redirect('base:listar_desafios')


@login_required
@permission_required('base.add_desafio', raise_exception=True)
def cadastrar_desafio(request):
    if request.method == 'POST':
        form = DesafioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print('Formulário válido, redirecionando...')
            return redirect('base:listar_desafios')
        else:
            print('Erros no formulário:', form.errors)
    else:
        form = DesafioForm()
    return render(request, 'base/cadastrar_desafio.html', {'form': form})


@login_required
@permission_required('base.add_corretor', raise_exception=True)
def cadastrar_corretor(request):
    if request.method == 'POST':
        form = CorretorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('base:listar_desafios')
        else:
            print('Erros no formulário:', form.errors)
    else:
        form = CorretorForm()
    return render(request, 'base/cadastrar_corretor.html', {'form': form})


@login_required
@require_corretor
def gerenciar_usuarios(request):
    corretores = Corretor.objects.all()
    return render(request, 'base/gerenciar_usuarios.html', {'corretores': corretores})


@login_required
@require_corretor
def editar_usuario(request, id):
    corretor = get_object_or_404(Corretor, id=id)
    if request.method == 'POST':
        form = CorretorForm(request.POST, instance=corretor)
        if form.is_valid():
            form.save()
            return redirect('base:gerenciar_usuarios')
    else:
        form = CorretorForm(instance=corretor)
    return render(request, 'base/editar_usuario.html', {'form': form})


@login_required
def atribuir_desafio(request):
    if request.method == 'POST':
        form = AtribuirDesafioForm(request.POST)
        if form.is_valid():
            try:
                corretor = Corretor.objects.get(cpf=form.cleaned_data['cpf'])
                desafio = form.cleaned_data['desafio']
                ParticipacaoDesafio.objects.create(corretor=corretor, desafio=desafio)
                messages.success(request, 'Desafio atribuído com sucesso.')
                return redirect('base:listar_desafios')
            except Corretor.DoesNotExist:
                form.add_error('cpf', 'Corretor não encontrado.')
            except Exception as e:
                messages.error(request, f'Erro ao atribuir o desafio: {str(e)}')
    else:
        form = AtribuirDesafioForm()
    return render(request, 'base/atribuir_desafio.html', {'form': form})


@login_required
@require_corretor
def visualizar_desafios_atribuidos(request):
    participacoes = ParticipacaoDesafio.objects.filter(corretor=request.corretor)
    return render(request, 'base/visualizar_desafios_atribuidos.html', {'participacoes': participacoes})
