from agencia import procurar_agencia
from cliente import procurar_cliente

'''O cadastro de conta exige um cliente cadastrado anteriormente'''
def cadastrar_conta(lista_clientes, lista_agencias, lista_contas):
    cpf = input("CPF do cliente: ")
    if not procurar_cliente(lista_clientes, cpf):
        print("Cliente não encontrado!")
        return None

    agencia_cod = input("Código da agência: ")
    if not procurar_agencia(lista_agencias, agencia_cod):
        print("Agência não encontrada!")
        return None

    numero = str(input("Insira o numero da conta: "))
    print(f"Conta {numero} criada com sucesso!")
    return (numero, cpf, agencia_cod, 0.0)