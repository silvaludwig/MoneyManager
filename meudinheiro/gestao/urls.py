from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import cadastro_usuario, custom_logout

urlpatterns = [
    # Páginas principais
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # Rotas para Despesas (usando pk em vez de id para padronização)
    path("despesas/", views.lista_despesas, name="lista_despesas"),
    path("despesas/nova/", views.nova_despesa, name="nova_despesa"),
    path("despesas/editar/<int:pk>/", views.editar_despesa, name="editar_despesa"),
    path("despesas/excluir/<int:pk>/", views.excluir_despesa, name="excluir_despesa"),
    path("despesas/<int:pk>/", views.detalhe_despesa, name="detalhe_despesa"),
    
    # Rotas para Receitas
    path("receitas/", views.lista_receitas, name="lista_receitas"),
    path("receitas/nova/", views.nova_receita, name="nova_receita"),
    path("receitas/editar/<int:pk>/", views.editar_receita, name="editar_receita"),
    path("receitas/excluir/<int:pk>/", views.excluir_receita, name="excluir_receita"),
    path("receitas/<int:pk>/", views.detalhe_receita, name="detalhe_receita"),

    # Rotas para Contas
    path("contas/", views.lista_contas, name="lista_contas"),
    path("contas/nova/", views.nova_conta, name="nova_conta"),
    path("contas/editar/<int:pk>/", views.editar_conta, name="editar_conta"),
    path("contas/excluir/<int:pk>/", views.excluir_conta, name="excluir_conta"),
    path("contas/<int:pk>/", views.detalhe_conta, name="detalhe_conta"),

    # Autenticação
    path("login/", auth_views.LoginView.as_view(
        template_name='gestao/auth/login.html',
        extra_context={'title': 'Login'}
    ), name="login"),
    # path("logout/", auth_views.LogoutView.as_view(
    #     template_name='gestao/auth/logout.html',
    #     extra_context={'title': 'Logout'}
    # ), name="logout"),
    # Custom logout view
    path('logout/', custom_logout, name='logout'),
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name='gestao/auth/password_reset.html',
        email_template_name='gestao/auth/password_reset_email.html',
        subject_template_name='gestao/auth/password_reset_subject.txt',
        extra_context={'title': 'Redefinir Senha'}
    ), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name='gestao/auth/password_reset_done.html',
        extra_context={'title': 'Email enviado'}
    ), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name='gestao/auth/password_reset_confirm.html',
        extra_context={'title': 'Nova senha'}
    ), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name='gestao/auth/password_reset_complete.html',
        extra_context={'title': 'Senha redefinida'}
    ), name="password_reset_complete"),
    path("password_change/", auth_views.PasswordChangeView.as_view(
        template_name='gestao/auth/password_change.html',
        extra_context={'title': 'Alterar senha'}
    ), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(
        template_name='gestao/auth/password_change_done.html',
        extra_context={'title': 'Senha alterada'}
    ), name="password_change_done"),

    # Cadastro de usuário
    path("cadastro/", cadastro_usuario, name="cadastro_usuario"),
]