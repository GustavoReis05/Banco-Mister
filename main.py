import agencia
import cliente
import conta

lista_clientes = []
lista_agencias = []
lista_contas = []



def menu_principal():
    # Carrega os dados persistidos na inicialização
    conta.carregar_dados_json(lista_clientes, lista_agencias, lista_contas)


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
            nova_conta = conta.cadastrar_conta(lista_clientes, lista_agencias)
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

        elif opcao == "7":
            conta.sacar(lista_contas)

        elif opcao == "8":
            conta.depositar(lista_contas)

        elif opcao == "9":
            conta.transferir(lista_contas)

        elif opcao == "10":
            conta.consultar_saldo(lista_contas)

        elif opcao == "11":
            codigo = input("Digite o código da agência: ").strip()
            agencia_econtrada= agencia.procurar_agencia(lista_agencias, codigo)
            if agencia_econtrada:
                total = conta.calcular_montante_agencia(lista_contas, codigo)
                print(
                    f"Montante Total na Agência {agencia_econtrada[0]} ({agencia_econtrada[1]}): R$ {total:.2f}"
                )
            else:
                print("Agência não encontrada.")

        elif opcao == "12":
            total_banco = conta.calcular_montante_banco(lista_contas)
            print(f"Montante Total no Banco Mister: R$ {total_banco:.2f}")

        elif opcao == "0":
            # Salva no arquivo json antes de encerrar
            conta.salvar_dados_json(
                lista_clientes, lista_agencias, lista_contas
            )
            print("Dados salvos em banco_dados.json com sucesso!")
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")

menu_principal()
