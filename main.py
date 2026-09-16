import agencia
import cliente
import conta

lista_clientes = []
lista_agencias = []
lista_contas = []

def menu_principal():

    while True:
        print("\n=== BANCO MISTER ===")
        print("1 - Cadastrar Cliente")
        print("2 - Cadastrar Agência")
        print("3 - Cadastrar Conta")
        print("4 - Listar Clientes")
        print("5 - Listar Agências")
        print("6 - Listar Contas")
        print("7 - Sacar")
        print("8 - Depositar")
        print("9 - Transferir")
        print("10 - Consultar Saldo")
        print("11 - Relatório: Montante Total da Agência")
        print("12 - Relatório: Montante Total do Banco")
        print("0 - Sair e Salvar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            novo_cliente = cliente.cadastrar_cliente()
            if novo_cliente:
                lista_clientes.append(novo_cliente)
                print(novo_cliente)

        elif opcao == "2":
            nova_agencia = agencia.cadastrar_agencia()
            if nova_agencia:
                lista_agencias.append(nova_agencia)
                print(nova_agencia)

        elif opcao == "3":
            nova_conta = conta.cadastrar_conta(lista_clientes, lista_agencias, lista_contas)
            if nova_conta:
                lista_contas.append(nova_conta)
                
        elif opcao == "4":
            if not lista_clientes:
                print("\nNenhum cliente cadastrado.")
            else:
                print("\n=== LISTA DE CLIENTES ===")
                for i in range(len(lista_clientes)):
                    print(f"{i + 1}. {lista_clientes[i]}")

        elif opcao == "5":
            if not lista_agencias:
                print("\nNenhuma agência cadastrada.")
            else:
                print("\n=== LISTA DE AGÊNCIAS ===")
                for i in range(len(lista_agencias)):
                    print(f"{i + 1}. {lista_agencias[i]}")

        elif opcao == "6":
            if not lista_contas:
                print("\nNenhuma conta cadastrada.")
            else:
                print("\n=== LISTA DE CONTAS ===")
                for i in range(len(lista_contas)):
                    print(f"{i + 1}. {lista_contas[i]}")

menu_principal()
