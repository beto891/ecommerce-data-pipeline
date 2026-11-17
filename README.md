# Documentação do Projeto: E-commerce Data Pipeline & Analytics

> Um ecossistema moderno de engenharia de dados, microsserviço transacional e painel analítico em tempo real, desenvolvido em Python.

---

## Visão Geral do Projeto

Este projeto foi concebido para simular o ciclo de vida completo dos dados em um ambiente de e-commerce corporativo. O sistema abrange desde a persistência relacional modelada em **Star Schema**, passando por uma API REST para ingestão e validação de regras de negócio, um simulador autônomo de tráfego transacional (gerando vendas em loop), até uma interface analítica interativa em tempo real construída com **Streamlit** e **Plotly**.

---

## Arquitetura e Estrutura de Pastas

A arquitetura do projeto segue o princípio de separação de responsabilidades (Modular Architecture):

```text
ecommerce-data-pipeline/
│
├── database/               # Camada de Persistência e DDL
│   ├── conexao.py          # Gerenciamento centralizado de conexões (Pathlib)
│   ├── tabelas.py          # Criação do Star Schema (Dimensões e Fato)
│   └── ecommerce.db        # Banco de dados local SQLite
│
├── api/                    # Camada de Ingestão e Regras de Negócio
│   └── main.py             # API REST (FastAPI) com validações Pydantic e ETL via Pandas
│
├── producer/               # Camada de Simulação de Tráfego
│   └── simula_dados.py     # Script produtor autônomo de pedidos em tempo real
│
├── dashboard/              # Camada de Visualização e BI
│   └── app.py              # Aplicação web executiva em Streamlit & Plotly
│
├── requirements.txt        # Dependências e bibliotecas do projeto
└── README.md               # Documentação principal para o GitHub
```
## Componentes do Ecossistema

### 1. Camada de Dados (database/)
Modelo Dimensional (Star Schema):
dim_clientes: Cadastro de clientes com informações demográficas (nome, e-mail, cidade, estado).
dim_produtos: Catálogo de produtos com categorias, preços de custo e preços de venda.
fato_pedidos: Tabela transacional que armazena os eventos de compra, quantidades, fretes calculados e chaves estrangeiras.
Conexão Segura: Utilização de pathlib para gerenciamento robusto de caminhos absolutos no sistema operacional.
### 2. Camada de Ingestão (api/)
Desenvolvida em FastAPI, atuando como o endpoint oficial para recebimento de pedidos.
Realiza validações rígidas de carga utilizando Pydantic.
Processa o cálculo automatizado de receita e lucro bruto através de manipulação de dados com Pandas antes de persistir no SQLite.
### 3. Simulação de Tráfego (producer/)
Script autônomo em Python (requests) que simula o comportamento de múltiplos clientes comprando na plataforma.
Dispara requisições POST em intervalos dinâmicos para a API FastAPI, povoando o banco de dados de forma contínua para testes em tempo real.
### 4. Camada de Apresentação (dashboard/)
Dashboard Executivo em Streamlit: Interface web moderna com tema corporativo.
Gráficos Dinâmicos (Plotly): Visualizações interativas de receita por categoria e evolução temporal do fluxo de pedidos.
KPIs em Tempo Real: Blocos executivos contendo Receita Total, Volume de Pedidos, Ticket Médio e Frete Médio com atualização automática (ttl).
Como Executar o Ecossistema Completo
Para rodar todo o pipeline integrando os componentes, são necessários 3 terminais simultâneos (com o ambiente virtual .venv ativado em todos):
Terminal 1 — Iniciar a API FastAPI:
uvicorn api.main:app --reload

Terminal 2 — Iniciar o Simulador de Tráfego:
python producer/simula_dados.py

Terminal 3 — Iniciar o Dashboard Interativo (Streamlit):
streamlit run dashboard/app.py

🛠️ Tecnologias Utilizadas
Linguagem: Python 3.14+
Banco de Dados: SQLite (Star Schema)
API & Validação: FastAPI, Pydantic, Uvicorn
Engenharia & Manipulação de Dados: Pandas, Requests

Visualização & Front-end: Streamlit, Plotly
