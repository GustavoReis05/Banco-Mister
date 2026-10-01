def cadastrar_cliente():
    #Funçao que cadastra clientes e os salva dentro de um dicionario com as chaves e valores correspondentes 
    while True:
        cpf = input("CPF: \n").strip()
        nome = input("Nome completo: \n")
        data_nascimento = input("Data de nascimento: \n")
        numero_telefone = input("Número de telefone: \n")

        print("\nOs dados estão corretos?\n")
        print("CPF: ", cpf)
        print("Nome completo: ", nome)
        print("Data de Nascimento: ", data_nascimento)
        print("Numero de Telefone: ", numero_telefone)
        print()

        while True:
            # Confirmaçao dados cadastrados
            confirmacao = input(
                "DIGITE A OPÇÃO DE ACORDO COM A VALIDADE DOS SEUS DADOS:\n"
                "1 - Sim, os dados estão corretos.\n"
                "2 - Não, os dados estão incorretos\n"
            ).strip()

            if confirmacao == "1":
                print("CLIENTE CADASTRADO COM SUCESSO!")
                return {
                    "cpf": cpf,
                    "nome": nome,
                    "data_nascimento": data_nascimento,
                    "numero_telefone": numero_telefone
                }
            elif confirmacao == "2":
                print("CADASTRE SEUS DADOS NOVAMENTE!")
                break
            else:
                print("Opção inválida! Digite 1 ou 2.")


def procurar_cliente(lista_clientes, termo_busca):
    """Busca um cliente pelo cpf ou nome"""
    for cliente in lista_clientes:
        if cliente['cpf'] == termo_busca or cliente['nome'] == termo_busca:
            return cliente
    return None