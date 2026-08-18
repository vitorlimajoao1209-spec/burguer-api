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
## 📌 6. Endpoints da API / API Endpoints

Abaixo estão as principais rotas disponíveis na aplicação. Você pode testá-las interativamente acessando `/docs` com o projeto rodando.

| Método | Rota | Descrição (PT-BR) | Description (EN) |
| :--- | :--- | :--- | :--- |
| **GET** | `/login` | Autentica a sessão com as credenciais padrão. | Authenticates session with default credentials. |
| **POST** | `/nova_senha` | Altera a senha de acesso com validação. | Changes access password with validation. |
| **GET** | `/produtos` | Lista todos os lanches cadastrados. | Lists all registered items. |
| **POST** | `/produtos` | Adiciona um novo item ao estoque. | Adds a new item to inventory. |
| **PUT** | `/produtos/{id}` | Atualiza a quantidade de um produto. | Updates a product's quantity. |
| **DELETE**| `/produtos/{id}` | Remove um item do sistema. | Removes an item from the system. |
| **POST** | `/vendas` | Registra venda e abate do estoque. | Records a sale and reduces stock. |
| **GET** | `/historico` | Exibe o relatório de logs e vendas. | Displays log and sales report. |

### 📄 7. Licença e Propósito / License & Purpose

**PT-BR:** Este projeto foi desenvolvido exclusivamente para fins de aprendizado próprio e demonstração de habilidades. Sinta-se livre para estudar o código e reutilizar os comandos, a lógica do FastAPI ou a sintaxe do Python em suas próprias aplicações. Contudo, **é proibido copiar e colar o projeto de forma idêntica**. Isso inclui replicar toda a estrutura da hamburgueria exatamente igual, com as mesmas rotas, definições de estoque e nomes inventados. Use o código para aprender os comandos, mas crie o seu próprio projeto. 

**EN:** This project was developed exclusively for self-learning purposes and to demonstrate skills. Feel free to study the code and reuse the commands, FastAPI logic, or Python syntax in your own applications. However, **copying and pasting the project identically is prohibited**. This includes replicating the entire burger shop structure exactly the same, with the same routes, inventory definitions, and invented names. Use the code to learn the commands, but build your own project.
