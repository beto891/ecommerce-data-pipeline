import sqlite3  # noqa: I001
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'database' / 'ecommerce.db'


def obter_conexao():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(DB_PATH)
    print("Conexão com o banco de dados estabelecida com sucesso.")
    return conexao

