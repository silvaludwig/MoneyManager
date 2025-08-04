from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from .models import Conta, Despesa, Receita
from .forms import ReceitaForm, DespesaForm, ContaForm
from django.contrib.auth import login, logout
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])  # Permite ambos os métodos temporariamente
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    # Se for GET, mostra a página de confirmação
    return render(request, 'gestao/auth/logout.html')

@login_required
def index(request):
    return render(request, "gestao/index.html")

@login_required
def dashboard(request):
    # Cálculos para o dashboard
    hoje = timezone.now().date()
    
    # Receitas
    total_receitas = Receita.objects.filter(
        usuario=request.user,
        data_vencimento__lte=hoje,
        efetivada=True
    ).aggregate(Sum('valor'))['valor__sum'] or 0
    
    # Despesas
    total_despesas = Despesa.objects.filter(
        usuario=request.user,
        data_vencimento__lte=hoje,
        efetivada=True
    ).aggregate(Sum('valor'))['valor__sum'] or 0
    
    saldo = total_receitas - total_despesas
    
    # Últimas transações
    ultimas_receitas = Receita.objects.filter(
        usuario=request.user
    ).order_by('-data_vencimento')[:5]
    
    ultimas_despesas = Despesa.objects.filter(
        usuario=request.user
    ).order_by('-data_vencimento')[:5]
    
    context = {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
        'ultimas_receitas': ultimas_receitas,
        'ultimas_despesas': ultimas_despesas,
        'contas': Conta.objects.filter(usuario=request.user, ativa=True),
    }
    return render(request, "gestao/dashboard.html", context)

# VIEWS DE RECEITA (já implementadas)
@login_required
def lista_receitas(request):
    receitas = Receita.objects.filter(usuario=request.user).order_by('-data_vencimento')
    return render(request, "receita/lista.html", {'receitas': receitas})

@login_required
def nova_receita(request):
    if request.method == "POST":
        form = ReceitaForm(request.POST, user=request.user)
        if form.is_valid():
            receita = form.save(commit=False)
            receita.usuario = request.user
            receita.save()
            messages.success(request, "Receita cadastrada com sucesso!")
            return redirect('lista_receitas')
    else:
        form = ReceitaForm(user=request.user)
    return render(request, "receita/formulario.html", {
        'form': form, 
        'titulo': 'Nova Receita'
    })

@login_required
def editar_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk, usuario=request.user)
    if request.method == "POST":
        form = ReceitaForm(request.POST, instance=receita, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Receita atualizada com sucesso!")
            return redirect('lista_receitas')
    else:
        form = ReceitaForm(instance=receita, user=request.user)
    return render(request, "receita/formulario.html", {
        'form': form,
        'titulo': 'Editar Receita'
    })

@login_required
def excluir_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk, usuario=request.user)
    if request.method == "POST":
        receita.delete()
        messages.success(request, "Receita excluída com sucesso!")
        return redirect('lista_receitas')
    return render(request, "receita/confirmar_delete.html", {'receita': receita})

@login_required
def detalhe_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk, usuario=request.user)
    return render(request, "receita/detalhe.html", {'receita': receita})

# VIEWS DE DESPESA (implementando as que faltam)
@login_required
def lista_despesas(request):
    despesas = Despesa.objects.filter(usuario=request.user).order_by('-data_vencimento')
    return render(request, "despesa/lista.html", {'despesas': despesas})

@login_required
def nova_despesa(request):
    if request.method == "POST":
        form = DespesaForm(request.POST, user=request.user)
        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.usuario = request.user
            despesa.save()
            messages.success(request, "Despesa cadastrada com sucesso!")
            return redirect('lista_despesas')
    else:
        form = DespesaForm(user=request.user)
    return render(request, "despesa/formulario.html", {
        'form': form,
        'titulo': 'Nova Despesa'
    })

@login_required
def editar_despesa(request, pk):
    despesa = get_object_or_404(Despesa, pk=pk, usuario=request.user)
    if request.method == "POST":
        form = DespesaForm(request.POST, instance=despesa, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Despesa atualizada com sucesso!")
            return redirect('lista_despesas')
    else:
        form = DespesaForm(instance=despesa, user=request.user)
    return render(request, "despesa/formulario.html", {
        'form': form,
        'titulo': 'Editar Despesa'
    })

@login_required
def excluir_despesa(request, pk):
    despesa = get_object_or_404(Despesa, pk=pk, usuario=request.user)
    if request.method == "POST":
        despesa.delete()
        messages.success(request, "Despesa excluída com sucesso!")
        return redirect('lista_despesas')
    return render(request, "despesa/confirmar_delete.html", {'despesa': despesa})

@login_required
def detalhe_despesa(request, pk):
    despesa = get_object_or_404(Despesa, pk=pk, usuario=request.user)
    return render(request, "despesa/detalhe.html", {'despesa': despesa})

# VIEWS DE CONTAS (implementando as que faltam)
@login_required
def lista_contas(request):
    contas = Conta.objects.filter(usuario=request.user).order_by('-data_criacao')
    return render(request, "conta/lista.html", {'contas': contas})

@login_required
def nova_conta(request):
    if request.method == "POST":
        form = ContaForm(request.POST, user=request.user)
        if form.is_valid():
            conta = form.save(commit=False)
            conta.usuario = request.user
            conta.save()
            messages.success(request, "Conta cadastrada com sucesso!")
            return redirect('lista_contas')
    else:
        form = ContaForm(user=request.user)
    return render(request, "conta/formulario.html", {
        'form': form,
        'titulo': 'Nova Conta'
    })

@login_required
def editar_conta(request, pk):
    conta = get_object_or_404(Conta, pk=pk, usuario=request.user)
    if request.method == "POST":
        form = ContaForm(request.POST, instance=conta, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta atualizada com sucesso!")
            return redirect('lista_contas')
    else:
        form = ContaForm(instance=conta, user=request.user)
    return render(request, "conta/formulario.html", {
        'form': form,
        'titulo': 'Editar Conta'
    })

@login_required
def excluir_conta(request, pk):
    conta = get_object_or_404(Conta, pk=pk, usuario=request.user)
    if request.method == "POST":
        conta.delete()
        messages.success(request, "Conta excluída com sucesso!")
        return redirect('lista_contas')
    return render(request, "conta/confirmar_delete.html", {'conta': conta})

@login_required
def detalhe_conta(request, pk):
    conta = get_object_or_404(Conta, pk=pk, usuario=request.user)
    return render(request, "conta/detalhe.html", {'conta': conta})

# VIEW DE CADASTRO DE USUÁRIO (descomentada e implementada)
from django.contrib.auth.forms import UserCreationForm
from .forms import CadastroUsuarioForm

def cadastro_usuario(request):
    if request.method == "POST":
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('index')
    else:
        form = CadastroUsuarioForm()
    return render(request, "gestao/auth/cadastro.html", {"form": form})