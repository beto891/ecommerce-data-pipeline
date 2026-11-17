from datetime import datetime, timedelta
import random
import requests
import time


URL_API = "http://localhost:8000/pedidos"

CLIENTES_IDS = list(range(1, 13))
PRODUTOS_IDS = list(range(1, 13))

TABELA_PRECOS = {
    1: 1200.00,  # Smartphone
    2: 150.00,   # Fone
    3: 80.00,    # Mouse
    4: 220.00,   # Teclado
    5: 1100.00,  # Monitor
    6: 650.00,   # Cadeira
    7: 450.00,   # Mesa
    8: 180.00,   # Cafeteira
    9: 320.00,   # Air Fryer
    10: 850.00,  # Robô Aspirador
    11: 120.00,  # Mochila
    12: 200.00   # Tênis
}

def gerar_data_futura():
    """Gera uma data de entrega prevista entre 3 a 10 dias no futuro."""
    dias_a_frente = random.randint(3, 10)
    data_futura = datetime.now() + timedelta(days= dias_a_frente)
    return data_futura.strftime("%Y-%m-%d")

def simular_envio_pedido():
    cliente_id = random.choice(CLIENTES_IDS)
    produto_id = random.choice(PRODUTOS_IDS)
    quantidade = random.randint(1, 3)

    preco_unitario = TABELA_PRECOS.get(produto_id, 100)

    valor_frete = random.choice([0.00, 15.50, 25.00, 40.00])

    data_entrega_prevista = gerar_data_futura()

    payload = {
        "cliente_id": cliente_id,
        "produto_id": produto_id,
        "quantidade": quantidade,
        "preco_unitario": preco_unitario,
        "valor_frete": valor_frete,
        "data_entrega_prevista": data_entrega_prevista
    }

    try:
            # Envia o POST para a nossa API FastAPI
            resposta = requests.post(URL_API, json=payload, timeout=5)
            
            if resposta.status_code == 201:
                dados_resposta = resposta.json()
                print(f"[SUCESSO] Pedido criado! Cliente {cliente_id} comprou Produto {produto_id} | "
                    f"Receita: R$ {dados_resposta['receita_calculada']:.2f} | "
                    f"Lucro: R$ {dados_resposta['lucro_calculado']:.2f}")
            else:
                print(f"[ERRO API] Status {resposta.status_code}: {resposta.text}")

    except requests.exceptions.ConnectionError:
            print("[FALHA DE CONEXÃO] A API FastAPI não está rodando ou está inacessível. Verifique o Uvicorn!")
    except Exception as e:
            print(f"[ERRO INESPERADO]: {e}")

if __name__ == "__main__":
    print("--- INICIANDO SIMULADOR DE PEDIDOS (PRODUCER) ---")
    print("Pressione Ctrl+C para parar a qualquer momento.\n")
    
    try:
        while True:
            simular_envio_pedido()
            # Aguarda entre 2 a 5 segundos antes de disparar o próximo pedido
            tempo_espera = random.randint(2, 5)
            time.sleep(tempo_espera)
            
    except KeyboardInterrupt:
        print("\n--- SIMULADOR ENCERRADO PELO USUÁRIO ---")