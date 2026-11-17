import sqlite3
from datetime import datetime
import pandas as pd
import plotly.express as px  # type: ignore
import streamlit as st

# 1. Configuração da Página (Layout Largo para aproveitar a tela)
st.set_page_config(
    page_title="Analytics E-commerce | Corporativo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS customizada leve para refinar o visual corporativo
st.markdown("""
    <style>
        .main {
            background-color: #0F172A;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=5)
def carregar_dados():
    conexao = sqlite3.connect("database/ecommerce.db")
    query = """
        SELECT 
            f.pedido_id, f.data_pedido, f.quantidade, f.preco_unitario, f.valor_frete,
            p.nome_produto, p.categoria, c.nome as cliente, c.cidade, c.estado
        FROM fato_pedidos f
        JOIN dim_produtos p ON f.produto_id = p.produto_id
        JOIN dim_clientes c ON f.cliente_id = c.cliente_id
    """
    df = pd.read_sql(query, conexao)
    conexao.close()
    
    if not df.empty:
        # Criação de colunas analíticas derivadas no Pandas
        df['data_pedido'] = pd.to_datetime(df['data_pedido'])
        df['receita_total'] = df['quantidade'] * df['preco_unitario']
        
    return df

df_pedidos = carregar_dados()

# 1. Cabeçalho
st.title("📊 Painel Executivo de Vendas & Logística")
st.markdown("Monitoramento em tempo real do fluxo de pedidos, receita e desempenho de categorias.")
st.markdown("---")

if df_pedidos.empty:
    st.warning("⚠️ Nenhum pedido registrado na base de dados no momento. Execute o seu script simulador (`producer/simula_dados.py`) para popular o banco!")
else:
    # 2. Seção de KPIs (Indicadores Chave de Desempenho)
    receita_total = df_pedidos['receita_total'].sum()
    total_pedidos = len(df_pedidos)
    ticket_medio = receita_total / total_pedidos if total_pedidos > 0 else 0
    frete_medio = df_pedidos['valor_frete'].mean()

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Receita Total", value=f"R$ {receita_total:,.2f}")
    with col2:
        st.metric(label="Volume de Pedidos", value=f"{total_pedidos:,}")
    with col3:
        st.metric(label="Ticket Médio", value=f"R$ {ticket_medio:,.2f}")
    with col4:
        st.metric(label="Frete Médio", value=f"R$ {frete_medio:,.2f}")

    st.markdown("---")

    # 3. Seção de Gráficos Analíticos com Plotly
    col_grafico1, col_grafico2 = st.columns(2)

    with col_grafico1:
        st.subheader("📦 Receita por Categoria de Produto")
        # Agrupa dados para o gráfico de barras
        df_categoria = df_pedidos.groupby('categoria')['receita_total'].sum().reset_index()
        
        fig_cat = px.bar(
            df_categoria, 
            x='categoria', 
            y='receita_total',
            text_auto='.2s',
            color='categoria',
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_cat.update_layout(
            showlegend=False,
            xaxis_title="Categoria",
            yaxis_title="Receita Total (R$)",
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_grafico2:
        st.subheader("📈 Evolução de Vendas por Pedido")
        # Gráfico de linha ordenado pelo ID/Tempo do pedido
        fig_linha = px.line(
            df_pedidos.sort_values('pedido_id'),
            x='pedido_id',
            y='receita_total',
            markers=True,
            line_shape='spline'
        )
        fig_linha.update_layout(
            xaxis_title="ID do Pedido",
            yaxis_title="Valor do Pedido (R$)",
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_linha, use_container_width=True)

    # 4. Tabela Detalhada com Recursos de Expansão
    st.markdown("### 📋 Histórico Detalhado de Transações")
    st.dataframe(
        df_pedidos[['pedido_id', 'data_pedido', 'cliente', 'estado', 'nome_produto', 'categoria', 'quantidade', 'receita_total', 'valor_frete']]
        .sort_values('pedido_id', ascending=False),
        use_container_width=True,
        hide_index=True
    )

    if st.button("🔄 Atualizar Dados Agora"):
        st.rerun()
