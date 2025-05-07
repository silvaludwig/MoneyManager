from django.shortcuts import render


def index(request):
    return render(request, "gestao/index.html")


def dashboard(request):
    return render(request, "gestao/dashboard.html")


# VIEWS DE RECEITA

def lista_receitas(request):
    return render(request, "receita/lista.html")

def nova_receita(request):
    return render(request, "receita/formulario.html")

def editar_receita(request):
    return render(request, "receita/formulario.html")

def excluir_receita(request):
    return render(request, "receita/confirmar_delete.html")

def detalhe_receita(request):
    return render(request, "receita/detalhe.html")


# VIEWS DE DESPESA

def lista_despesas(request):
    return render(request, "despesa/lista.html")

def nova_despesa(request):
    return render(request, "despesa/formulario.html")

def editar_despesa(request):
    return render(request, "despesa/formulario.html")

def excluir_despesa(request):
    return render(request, "despesa/confirmar_delete.html")

def detalhe_despesa(request):
    return render(request, "despesa/detalhe.html")


# VIEWS DE CONTAS

def lista_contas(request):
    return render(request, "conta/lista.html")

def nova_conta(request):
    return render(request, "conta/formulario.html")

def editar_conta(request):
    return render(request, "conta/formulario.html")

def excluir_conta(request):
    return render(request, "conta/confirmar_delete.html")

def detalhe_conta(request):
    return render(request, "conta/detalhe.html")