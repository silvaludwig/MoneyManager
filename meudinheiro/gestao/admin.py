from django.contrib import admin
from .models import Conta, Despesa, Receita, TransacaoImportada
from django.utils import timezone

@admin.action(description="Importar como Receita")
def importar_como_receita(modeladmin, request, queryset):
    for transacao in queryset.filter(tipo='credito', importada=False):
        Receita.objects.create(
            usuario=transacao.usuario,
            conta=transacao.conta,
            descricao=transacao.descricao,
            valor=transacao.valor,
            data_vencimento=transacao.data,
            efetivada=True,
            recorrente='unica',
            categoria='outros',
            origem=transacao.origem_api
        )
        transacao.importada = True
        transacao.save()

@admin.action(description="Importar como Despesa")
def importar_como_despesa(modeladmin, request, queryset):
    for transacao in queryset.filter(tipo='debito', importada=False):
        Despesa.objects.create(
            usuario=transacao.usuario,
            conta=transacao.conta,
            descricao=transacao.descricao,
            valor=transacao.valor,
            data_vencimento=transacao.data,
            efetivada=True,
            recorrente='unica',
            categoria='outros',
            parcelas=1,
            parcela_atual=1
        )
        transacao.importada = True
        transacao.save()

@admin.register(TransacaoImportada)
class TransacaoImportadaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'tipo', 'data', 'conta', 'importada')
    list_filter = ('tipo', 'importada', 'conta')
    search_fields = ('descricao',)
    actions = [importar_como_receita, importar_como_despesa]

# Já registrados
admin.site.site_header = "Meu Dinheiro - Administração"
admin.site.site_title = "Meu Dinheiro Admin"
admin.site.index_title = "Bem-vindo ao painel de administração do Meu Dinheiro"
admin.site.register(Conta)
admin.site.register(Despesa)
admin.site.register(Receita)
