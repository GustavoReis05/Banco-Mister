saldo = 0

def consulta_saldo():
    print("O saldo disponivel é: R$",saldo)

def deposito(entrada):
    saldo = saldo + entrada
    return saldo

def saque(saida):
    if saida > saldo:
        return "Valor indisponivel"
    else:
        saldo = saldo - saida
        return "SAQUE REALIZADO COM SUCESSO!"
