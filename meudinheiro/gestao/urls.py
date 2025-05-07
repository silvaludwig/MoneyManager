from django.urls import path
from . import views

urlpatterns = [
    # Páginas principais
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # Rotas para Despesas
    path("despesas/", views.lista_despesas, name="lista_despesas"),
    path("despesas/novo", views.nova_despesa, name="nova_despesa"),
    path("despesas/editar/<int:id>/", views.editar_despesa, name="editar_despesa"),
    path("despesas/excluir/<int:id>/", views.excluir_despesa, name="excluir_despesa"),
    path("despesas/<int:id>/", views.detalhe_despesa, name="detalhe_despesa"),
    
    # Rotas para Receitas
    path("receitas/", views.lista_receitas, name="lista_receitas"),
    path("receitas/novo", views.nova_receita, name="nova_receita"),
    path("receitas/editar/<int:id>/", views.editar_receita, name="editar_receita"),
    path("receitas/excluir/<int:id>/", views.excluir_receita, name="excluir_receita"),
    path("receitas/<int:id>/", views.detalhe_receita, name="detalhe_receita"),

    # Rotas para Contas
    path("contas/", views.lista_contas, name="lista_contas"),
    path("contas/novo", views.nova_conta, name="nova_conta"),
    path("contas/editar/<int:id>/", views.editar_conta, name="editar_conta"),
    path("contas/excluir/<int:id>/", views.excluir_conta, name="excluir_conta"),
    path("contas/<int:id>/", views.detalhe_conta, name="detalhe_conta"),

]
