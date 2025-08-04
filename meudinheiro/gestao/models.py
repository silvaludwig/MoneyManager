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
    
    id_externo = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID Externo da API"
    )

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

    conta = models.ForeignKey(
        Conta,
        on_delete=models.PROTECT,
        related_name='despesas'  # Isso cria o atributo despesas na Conta
    )


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

    conta = models.ForeignKey(
        Conta,
        on_delete=models.PROTECT,
        related_name='receitas'  # Isso cria o atributo receitas na Conta
    )
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

class ConexaoBancaria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome_banco = models.CharField(max_length=100)
    token_acesso = models.CharField(max_length=255)
    id_conexao_api = models.CharField(max_length=255, unique=True)  # ID da conexão na API externa
    data_conexao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome_banco} ({self.usuario.username})"
    
    class Meta:
        verbose_name = "Conexão Bancária"
        verbose_name_plural = "Conexões Bancárias"
        ordering = ['-data_conexao']
    
    

class TransacaoImportada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    data = models.DateField()
    tipo = models.CharField(max_length=10, choices=[('credito', 'Crédito'), ('debito', 'Débito')])
    origem_api = models.CharField(max_length=100, blank=True, null=True)
    categoria_api = models.CharField(max_length=100, blank=True, null=True)
    id_api = models.CharField(max_length=255, unique=True)
    importada = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Transação Importada"
        verbose_name_plural = "Transações Importadas"
        ordering = ['-data']
    
    def __str__(self):
        return f"{self.descricao} - R${self.valor} ({self.tipo})"
