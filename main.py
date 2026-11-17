from database.tabelas import criar_tabelas


def iniciar_sistema():
    print("Iniciando o sistema...")
    criar_tabelas()

if __name__ == "__main__":
    iniciar_sistema()