def cadastro_cliente ():
    cpf= input("CPF: ")
    nome = input("Nome completo: ")
    login = input("Login: ")
    senha = input("Senha: ")

    print("\n")

    print("Os dados estão corretos?")
    print("\n")
    print("CPF: ",cpf)
    print("Nome completo: ",nome)
    print("Login: ",login)
    print("Senha: ",senha)

    print("\n")

    confirmacao = int(input("DIGITE A OPÇÃO DE ACORDO COM A VALIDADE DOS SEUS DADOS: \n"
                            "1 - Sim, os dados estão corretos.\n" \
                            "2 - Não, os dados estão incorretos\n"))
    if confirmacao == 1:
        print("CONTA CRIADA COM SUCESSO!")
        return nome
    elif confirmacao == 2:
        print("QUE PENA! REINICIE O PROGRAMA PARA CRIARMOS SUA CONTA COM OS DADOS CORRETOS.")
        exit()
    else:
        print("OPÇÃO INVALIDA!")
        exit()

