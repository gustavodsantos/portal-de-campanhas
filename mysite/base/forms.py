from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Corretor, Desafio, User


class DesafioForm(forms.ModelForm):
    class Meta:
        model = Desafio
        fields = ['nome', 'descricao', 'banner', 'regras_pontuacao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'banner': forms.FileInput(attrs={'class': 'form-control custom-file-input'}),
            'regras_pontuacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Regras de Pontuação'}),
        }


class CorretorForm(forms.ModelForm):
    """Formulário para criar ou editar corretores"""

    nome = forms.CharField(max_length=64)

    class Meta:
        model = Corretor
        fields = ['nome', 'cpf']

    def save(self, commit=True):
        corretor = super().save(commit=False)
        user = corretor.user
        user.first_name = self.cleaned_data['nome']
        if commit:
            user.save()
            corretor.save()
        return corretor


class AtribuirDesafioForm(forms.Form):
    cpf = forms.CharField(max_length=11)
    desafio = forms.ModelChoiceField(queryset=Desafio.objects.all())


class RegistroUsuarioForm(UserCreationForm):
    """Formulário para cadastro de usuários"""

    nome = forms.CharField(max_length=64, label='Nome')
    cpf = forms.CharField(max_length=11, required=False, label='CPF (opcional, se deseja ser corretor)')

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'nome', 'cpf']

    def save(self, commit=True):
        user = super().save(commit=False)
        nome = self.cleaned_data['nome']
        cpf = self.cleaned_data.get('cpf')

        user.first_name = nome
        if commit:
            user.save()
            if cpf:  # Se o CPF foi preenchido, cria o perfil de corretor
                Corretor.objects.create(user=user, cpf=cpf)
        return user
