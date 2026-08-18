# burguer-api
API para gerenciamento de hamburgueria com FastAPI, SQLite e controle de estoque | Burger shop management API built with Python, FastAPI &amp; SQLite.
---

## 1. Descrição do Projeto / Project Description

### 1.1 Português
Uma API RESTful desenvolvida para simplificar e automatizar a gestão do dia a dia de uma hamburgueria. O projeto combina regras de negócio reais — como controle de estoque, histórico de movimentações, autenticação de administrador com trava de segurança e métricas de vendas — com uma arquitetura leve em Python e persistência em banco de dados SQLite.

* **Controle de Estoque:** Operações para adicionar, remover, atualizar e vender lanches com validação de quantidade.
* **Segurança:** Rotas protegidas por verificação de administrador, suporte a alteração de senha e encerramento após 3 tentativas incorretas.
* **Histórico de Operações:** Registro de logins, vendas, alterações de estoque e remoção de registros no banco de dados.
* **Persistência Confiável:** Armazenamento estruturado em tabelas SQLite.

### 1.2 English
A RESTful API designed to streamline day-to-day operations for a burger shop. This project pairs practical business logic—such as real-time inventory management, operation history logs, admin authentication with security cutoffs, and sales metrics—with a clean Python and FastAPI architecture backed by SQLite persistence.

* **Smart Inventory:** Endpoints to create, update, reduce, and sell items with stock availability checks.
* **Security Controls:** Protected endpoints via admin validation, password updates, and service cutoff after 3 failed login attempts.
* **Audit Logging:** Database-backed activity history tracking logins, sales events, stock changes, and log clears.
* **Reliable Persistence:** Structured SQLite tables to ensure data integrity.

---

## 2. Credenciais Padrão / Default Credentials

* **Login / Username:** JKLOG
* **Senha Padrão / Default Password:** 123JK

---

## 3. Passo a Passo de Uso / Usage Steps

1. Execute o arquivo principal da aplicação: `python main.py`
2. Abra a documentação interativa no navegador: `http://localhost:8000/docs`
3. Acesse o endpoint **GET /login** e insira as credenciais para autenticar a sessão.
4. Utilize as rotas protegidas para gerenciar o estoque e registrar vendas.
5. *(Opcional)* Altere a senha de acesso no endpoint **POST /nova_senha**.

---

## 4. Configurações e Ajustes / Configuration Steps

1. **Alterar o nome do banco:** Modifique a variável `BANCO_DADOS = "dados_sistema.db"` no arquivo `main.py`.
2. **Alterar usuário e senha iniciais:** Modifique os valores padrão dentro da função `iniciar_banco()`.
3. **Alterar porta de execução:** Altere os parâmetros na linha `uvicorn.run(app, host="0.0.0.0", port=8000)`.

---

## 5. Tecnologias Utilizadas / Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi&labelColor=white&color=009485)![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat&logo=sqlite&logoColor=white) ![Uvicorn](https://img.shields.io/badge/Uvicorn-44813B?style=flat&logo=uvicorn&logoSize=white)
