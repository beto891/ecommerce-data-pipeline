from datetime import datetime
from fastapi import FastAPI, HTTPException  # pyright: ignore[reportMissingImports] # noqa: I001
from pydantic import BaseModel, Field  # type: ignore
import pandas as pd  # type: ignore
from database.conexao import obter_conexao


app = FastAPI(
    title='API de ETL para o pipeline de dados do e-commerce', 
    version='1.0.0'
)

class PedidoInput(BaseModel):
    cliente_id: int
    produto_id: int
    quantidade: int = Field(..., gt=0, description="A quantidade deve ser maior que zero")
    preco_unitario: float = Field(..., gt=0, description="O preço unitário deve ser positivo")
    valor_frete: float = Field(..., ge=0, description="O frete não pode ser negativo")
    data_entrega_prevista: str  # Irá receber a data como string ex: 2026-01-01

# Rota POST de ingestão e ETL
@app.post("/pedidos", status_code=201)
def criar_pedidos(fato_pedido: PedidoInput):
    conexao = None
    try:
        # 1º Passo: transformar os dados recebidos em um DataFrame
        dados_dict = fato_pedido.dict()
        df = pd.DataFrame([dados_dict])

        # Transformação de criação de colunas derivadas
        df['receita_total'] = df['quantidade'] * df['preco_unitario']

        conexao = obter_conexao()
        cursor = conexao.cursor()

        # Validação de Data Quality: Verificar se o produto existe
        cursor.execute("SELECT custo_unitario FROM dim_produtos WHERE produto_id = ?", (int(df['produto_id'].iloc[0]),))
        produto_db = cursor.fetchone()

        if not produto_db:
            conexao.close()
            # Retorna o erro 400 controlado diretamente
            raise HTTPException(status_code=400, detail='Produto não encontrado na base de dados.')

        # Fluxo executado apenas quando o produto é encontrado (indentação correta)
        custo_unitario = produto_db[0]
        df['lucro_bruto'] = df['receita_total'] - (df['quantidade'] * custo_unitario)

        # Status inicial padrão do pedido
        status_pedido = "Em Trânsito"
        data_pedido = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO fato_pedidos (
                cliente_id, produto_id, data_pedido, data_entrega_prevista, 
                data_entrega_real, status_pedidos, quantidade, 
                preco_unitario, valor_frete
            ) VALUES (?, ?, ?, ?, NULL, ?, ?, ?, ?)
        """, (
            int(df['cliente_id'].iloc[0]),
            int(df['produto_id'].iloc[0]),
            data_pedido,
            df['data_entrega_prevista'].iloc[0],
            status_pedido,
            int(df['quantidade'].iloc[0]),
            float(df['preco_unitario'].iloc[0]),
            float(df['valor_frete'].iloc[0])
        ))
        
        conexao.commit()
        conexao.close()

        return {
            "mensagem": "Pedido processado e inserido com sucesso!",
            "receita_calculada": df['receita_total'].iloc[0],
            "lucro_calculado": df['lucro_bruto'].iloc[0]
        }

    except HTTPException as he:
        # Repassa exceções HTTP controladas (como o 400 de produto não encontrado) sem mascará-las como 500
        if conexao:
            conexao.close()
        raise he

    except Exception as e:
        if conexao:
            conexao.close()
            
        import traceback
        traceback.print_exc()
        
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
