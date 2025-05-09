# README - Sistema de Gerenciamento Financeiro Pessoal

## 📌 Visão Geral

O **Sistema de Gerenciamento Financeiro Pessoal** é uma aplicação Django desenvolvida para ajudar usuários a gerenciar suas finanças de forma eficiente, com controle completo sobre receitas, despesas e contas bancárias.

## ✨ Funcionalidades Principais

- **Controle Financeiro Completo**
  - Cadastro de receitas e despesas
  - Controle de contas bancárias
  - Dashboard com resumo financeiro

- **Recursos Avançados**
  - Sistema de parcelamento de despesas
  - Categorização de transações
  - Controle de status (efetivado/pendente)
  - Filtros e relatórios

- **Interface Moderna**
  - Tema escuro com ótimo contraste visual
  - Design responsivo para todos os dispositivos
  - Ícones intuitivos

## 🛠️ Tecnologias Utilizadas

- **Backend**
  - Python 3.x
  - Django 4.x
  - Django REST Framework (para futuras APIs)

- **Frontend**
  - Bootstrap 5 (com tema escuro personalizado)
  - Bootstrap Icons
  - HTML5 + CSS3 moderno

- **Banco de Dados**
  - SQLite (desenvolvimento)
  - PostgreSQL (produção recomendada)

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.8+
- Pipenv (ou virtualenv)

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/gestao-financeira.git
   cd gestao-financeira
   ```

2. Configure o ambiente virtual:
   ```bash
   pip install pipenv
   pipenv install
   pipenv shell
   ```

3. Aplique as migrações:
   ```bash
   python manage.py migrate
   ```

4. Crie um superusuário:
   ```bash
   python manage.py createsuperuser
   ```

5. Execute o servidor:
   ```bash
   python manage.py runserver
   ```

6. Acesse no navegador:
   ```
   http://localhost:8000
   ```

## 🏗️ Estrutura do Projeto

```
gestao-financeira/
├── gestao/                 # App principal
│   ├── templates/          # Templates base
│   ├── models.py           # Modelos de dados
│   ├── views.py            # Lógica das views
│   ├── forms.py            # Formulários
│   └── urls.py             # URLs do app
├── static/                 # Arquivos estáticos
├── manage.py
└── README.md
```

## 🔒 Sistema de Autenticação

- Cadastro de usuários
- Login/logout seguro
- Redefinição de senha
- Controle de permissões

## 📦 Dependências Principais

Listadas no `Pipfile`:
- Django
- django-crispy-forms
- django-environ
- psycopg2-binary (para PostgreSQL)

## 🌈 Temas e Personalização

O sistema utiliza um tema escuro personalizado com as seguintes variáveis CSS:

```css
:root {
    --bg-dark: #1a1a2e;
    --bg-darker: #16213e;
    --primary: #0f3460;
    --secondary: #533483;
    --accent: #e94560;
    --text-light: #f1f1f1;
}
```

## 🤝 Contribuição

Contribuições são bem-vindas! Siga os passos:

1. Faça um fork do projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.


