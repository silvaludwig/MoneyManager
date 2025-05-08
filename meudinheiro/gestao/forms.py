from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Despesa, Receita, Conta
from django.core.exceptions import ValidationError
from django.utils import timezone

class DespesaForm(forms.ModelForm):
    data_vencimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now().date()
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['conta'].queryset = Conta.objects.filter(usuario=self.user, ativa=True)
            self.fields['conta'].label_from_instance = lambda obj: f"{obj.nome} (Saldo: R$ {obj.saldo_atual:.2f})"

    class Meta:
        model = Despesa
        fields = ['descricao', 'valor', 'data_vencimento', 'categoria', 
                 'recorrente', 'conta', 'parcelas', 'observacoes']
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Descrição da despesa'}),
            'valor': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'valor': 'Valor (R$)',
        }

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor <= 0:
            raise ValidationError("O valor deve ser maior que zero")
        return valor


class ReceitaForm(forms.ModelForm):
    data_vencimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now().date()
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['conta'].queryset = Conta.objects.filter(usuario=self.user, ativa=True)
            self.fields['conta'].label_from_instance = lambda obj: f"{obj.nome} (Saldo: R$ {obj.saldo_atual:.2f})"

    class Meta:
        model = Receita
        fields = ['descricao', 'valor', 'data_vencimento', 'categoria', 
                 'recorrente', 'conta', 'origem', 'observacoes']
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Descrição da receita'}),
            'valor': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'valor': 'Valor (R$)',
        }


class ContaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Conta
        fields = ['nome', 'saldo_inicial', 'categoria']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome da conta'}),
            'saldo_inicial': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'saldo_inicial': 'Saldo Inicial (R$)',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.usuario = self.user
        if commit:
            instance.save()
        return instance


class CadastroUsuarioForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Seu melhor email'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nome de usuário'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email já está cadastrado")
        return email
