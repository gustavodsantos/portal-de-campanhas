from django import forms

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

    # Incluindo o campo do nome e email diretamente do modelo User
    nome = forms.CharField(max_length=64)
    email = forms.EmailField()

    class Meta:
        model = Corretor
        fields = ['nome', 'email', 'cpf']

    def save(self, commit=True):
        # Cria ou atualiza o usuário relacionado ao corretor
        corretor = super().save(commit=False)
        user_data = {'first_name': self.cleaned_data['nome'], 'email': self.cleaned_data['email']}

        if not corretor.user_id:  # Se ainda não houver um user associado
            user = User.objects.create(**user_data)
            corretor.user = user
        else:  # Atualiza o usuário existente
            for attr, value in user_data.items():
                setattr(corretor.user, attr, value)
            if commit:
                corretor.user.save()

        if commit:
            corretor.save()

        return corretor


class AtribuirDesafioForm(forms.Form):
    cpf = forms.CharField(max_length=11)
    desafio = forms.ModelChoiceField(queryset=Desafio.objects.all())
