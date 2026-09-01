"""Implantação de um menu para escolha da operação desejada"""
def operacao(saldo):
    menu_inicial = int(input("1 - CONSULTAR SALDO\n" 
                            "2 - REALIZAR DEPÓSITO\n"
                            "3 - REALIZAR SAQUE\n"))
    if menu_inicial == 1:
        print("O saldo disponivel é: R$",saldo)

    elif menu_inicial == 2:
        valor_dep = float(input("Valor do depósito: R$"))
        saldo = saldo + valor_dep
        print("Deposito realizado com sucesso!")

    elif menu_inicial == 3:
        valor_saque = float(input("Valor do saque: R$"))

        if valor_saque > saldo:
            print("Valor indisponivel")

        else:
            saldo = saldo - valor_saque
            print("SAQUE REALIZADO COM SUCESSO!") 

    else:
        print("OPERAÇÃO INVALIDA.")
        