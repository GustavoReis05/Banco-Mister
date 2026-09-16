def cadastrar_cliente():
    cpf= input("CPF: \n")
    nome = input("Nome completo: \n")
    data_nascimento = input("Data de nascimento: \n")
    numero_telefone = input("Número de telefone: \n")


    print("\n")
    
    print("Os dados estão corretos?")
    print("\n")
    print("CPF: ",cpf)
    print("Nome completo: ",nome)
    print("Data de Nascimento: ", data_nascimento)
    print("Numero de Telefone: ", numero_telefone)
    
    print("\n")
    
    confirmacao = int(input("DIGITE A OPÇÃO DE ACORDO COM A VALIDADE DOS SEUS DADOS: \n"
                            "1 - Sim, os dados estão corretos.\n" \
                            "2 - Não, os dados estão incorretos\n"))

    while confirmacao == 2:
        print("CADASTRE SEUS DADOS NOVAMENTE!")
        return cadastrar_cliente()

    if confirmacao == 1:
        print("CLIENTE CADASTRADO COM SUCESSO!")
        return cpf, nome, data_nascimento, numero_telefone
        exit()

def procurar_cliente(lista_clientes, cpf):
    """Busca um cliente na lista pelo cpf"""
    for cliente in lista_clientes:
        if cliente[0] == cpf:
            return cliente
    return None
