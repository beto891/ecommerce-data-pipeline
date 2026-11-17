from database.conexao import obter_conexao


def criar_tabelas(): 
    conexao = obter_conexao()
    cursor = conexao.cursor()
   
    sql_script = """
        CREATE TABLE IF NOT EXISTS dim_clientes (
            cliente_id INTEGER PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            cidade VARCHAR(50) NOT NULL,
            estado TEXT NOT NULL CHECK (estado IN 
            ('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 
            'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO')),
            segmento VARCHAR(100) NOT NULL);


        CREATE TABLE IF NOT EXISTS dim_produtos (
            produto_id INTEGER PRIMARY KEY,
            nome_produto VARCHAR(100) NOT NULL,
            categoria VARCHAR(100) NOT NULL,
            custo_unitario FLOAT NOT NULL);


        CREATE TABLE IF NOT EXISTS fato_pedidos (
            pedido_id INTEGER PRIMARY KEY NOT NULL,
            cliente_id INT NOT NULL,
            produto_id INT NOT NULL,
            data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
            data_entrega_prevista DATE NOT NULL,
            data_entrega_real DATE  NULL,
            status_pedidos NOT NULL
            DEFAULT 'Em Trânsito'
            CHECK (status_pedidos IN ('Processando', 'Em Trânsito', 'Entregue', 'Cancelado')),
            quantidade INT NOT NULL,
            preco_unitario FLOAT NOT NULL,
            valor_frete FLOAT NOT NULL,

            FOREIGN KEY(cliente_id) REFERENCES dim_produtos(id),
            FOREIGN KEY(produto_id) REFERENCES dim_produtos(id)
            );

        """  
    # noqa: F841, RUF100

    cursor.executescript(sql_script)
    conexao.commit()
    conexao.close()