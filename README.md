# ecommerce-data-pipeline
Ecossistema completo de engenharia e análise de dados em tempo real, desenvolvido em Python. Contém modelagem relacional em Star Schema (SQLite), API REST de ingestão com validações e ETL (FastAPI e Pandas), simulador autônomo de tráfego transacional (Producer) e painel executivo interativo (Streamlit e Plotly).

# 🚀 Documentação do Projeto: E-commerce Data Pipeline & Analytics

> Um ecossistema moderno de engenharia de dados, microsserviço transacional e painel analítico em tempo real, desenvolvido em Python.

---

## 📌 Visão Geral do Projeto

Este projeto foi concebido para simular o ciclo de vida completo dos dados em um ambiente de e-commerce corporativo. O sistema abrange desde a persistência relacional modelada em **Star Schema**, passando por uma API REST para ingestão e validação de regras de negócio, um simulador autônomo de tráfego transacional (gerando vendas em loop), até uma interface analítica interativa em tempo real construída com **Streamlit** e **Plotly**.

---

## 🏗️ Arquitetura e Estrutura de Pastas

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
