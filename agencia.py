def cadastrar_agencia():
    """Solicita os dados da agência e retorna uma tupla."""
    codigo = input("Código da Agência: \n")
    nome = input("Nome da Agência: \n")

    agencia = (codigo, nome)
    print("AGÊNCIA CADASTRADA COM SUCESSO!")
    return agencia