from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Conta(models.Model):
    CATEGORIA_CHOICES = [
        ('corrente', 'Conta Corrente'),
        ('pagamento', 'Conta de Pagamento'),
        ('carteira', 'Carteira'),
        ('poupanca', 'Poupança'),
        ('investimento', 'Investimento'),
    ]
    
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='contas'
    )
    nome = models.CharField(
        max_length=50, 
        verbose_name="Nome da Conta"
    )
    saldo_inicial = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)]
    )
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default="corrente",
        verbose_name="Tipo de Conta"
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    ativa = models.BooleanField(
        default=True,
        verbose_name="Conta Ativa?"
    )

    class Meta:
        verbose_name = "Conta"
        verbose_name_plural = "Contas"
        ordering = ['-data_criacao']

    def __str__(self):
        return f"{self.nome} ({self.get_categoria_display()})"

    @property
    def saldo_atual(self):
        # Calcula o saldo atual considerando todas as transações
        receitas = self.receitas.filter(efetivada=True).aggregate(
            total=models.Sum('valor'))['total'] or 0
        despesas = self.despesas.filter(efetivada=True).aggregate(
            total=models.Sum('valor'))['total'] or 0
        return self.saldo_inicial + receitas - despesas


class TransacaoBase(models.Model):
    RECORRENTE_CHOICES = [
        ('fixa', 'Fixa Mensal'),
        ('variavel', 'Variável'),
        ('unica', 'Única'),
    ]
    
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='%(class)s_transacoes'
    )
    descricao = models.CharField(
        max_length=100, 
        verbose_name="Descrição"
    )
    valor = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    data_vencimento = models.DateField(
        verbose_name="Data de Vencimento",
        default=timezone.now
    )
    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Registro"
    )
    efetivada = models.BooleanField(
        default=False,
        verbose_name="Efetivada?"
    )
    recorrente = models.CharField(
        max_length=20,
        choices=RECORRENTE_CHOICES,
        default="unica",
        verbose_name="Recorrência"
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações"
    )
    conta = models.ForeignKey(
        Conta,
        on_delete=models.PROTECT,
        related_name='%(class)s'
    )

    class Meta:
        abstract = True
        ordering = ['-data_vencimento']

    def __str__(self):
        return f"{self.descricao} - R${self.valor}"


class Despesa(TransacaoBase):
    CATEGORIA_CHOICES = [
        ('alimentacao', 'Alimentação'),
        ('transporte', 'Transporte'),
        ('moradia', 'Moradia'),
        ('saude', 'Saúde'),
        ('educacao', 'Educação'),
        ('lazer', 'Lazer'),
        ('vestuario', 'Vestuário'),
        ('servicos', 'Serviços'),
        ('impostos', 'Impostos'),
        ('pets', 'Pets'),
        ('outros', 'Outros'),
    ]

    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default="outros",
        verbose_name="Categoria"
    )
    parcelas = models.PositiveIntegerField(
        default=1,
        verbose_name="Número de Parcelas"
    )
    parcela_atual = models.PositiveIntegerField(
        default=1,
        verbose_name="Parcela Atual"
    )

    class Meta:
        verbose_name = "Despesa"
        verbose_name_plural = "Despesas"


class Receita(TransacaoBase):
    CATEGORIA_CHOICES = [
        ('salario', 'Salário'),
        ('freelance', 'Freelance'),
        ('investimentos', 'Investimentos'),
        ('comissao', 'Comissão'),
        ('vendas', 'Vendas'),
        ('presente', 'Presente'),
        ('beneficios', 'Benefícios'),
        ('outros', 'Outros'),
    ]

    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default="outros",
        verbose_name="Categoria"
    )
    origem = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Origem/Fonte"
    )

    class Meta:
        verbose_name = "Receita"
        verbose_name_plural = "Receitas"