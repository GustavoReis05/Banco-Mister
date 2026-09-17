import json
from agencia import procurar_agencia
from cliente import procurar_cliente

# Estrutura da Tupla: (numero_conta, cpf_cliente, codigo_agencia, saldo)


def cadastrar_conta(lista_clientes, lista_agencias):
    cpf = input("CPF do cliente: ")
    if not procurar_cliente(lista_clientes, cpf):
        print("Cliente não encontrado!")
        return None

    agencia_cod = input("Código da agência: ")
    if not procurar_agencia(lista_agencias, agencia_cod):
        print("Agência não encontrada!")
        return None

    numero_conta = int(input("Digite o numero da conta: "))
    print(f"Conta {numero_conta} criada com sucesso!")
    return (numero_conta, cpf, agencia_cod, 0.0)


def procurar_conta(lista_contas, numero):
    for c in lista_contas:
        if c[0] == numero:
            return c
    return None


def atualizar_saldo(lista_contas, numero, novo_saldo):
    for i, c in enumerate(lista_contas):
        if c[0] == numero:
            lista_contas[i] = (c[0], c[1], c[2], novo_saldo)
            break


def sacar(lista_contas):
    c = procurar_conta(lista_contas, input("Número da Conta: "))
    if not c:
        return print("Conta não encontrada!")

    valor = float(input("Valor do saque: R$ "))
    if 0 < valor <= c[3]:
        atualizar_saldo(lista_contas, c[0], c[3] - valor)
        print(f"Saque de R$ {valor:.2f} realizado!")
    else:
        print("Valor inválido ou saldo insuficiente.")


def depositar(lista_contas):
    c = procurar_conta(lista_contas, input("Número da Conta: "))
    if not c:
        return print("Conta não encontrada!")

    valor = float(input("Valor do depósito: R$ "))
    if valor > 0:
        atualizar_saldo(lista_contas, c[0], c[3] + valor)
        print(f"Depósito de R$ {valor:.2f} realizado!")
    else:
        print("Valor inválido.")


def transferir(lista_contas):
    origem = procurar_conta(lista_contas, input("Número da Conta Origem: "))
    destino = procurar_conta(lista_contas, input("Número da Conta Destino: "))

    if not origem or not destino:
        return print("Conta de origem ou destino não encontrada!")

    valor = float(input("Valor da transferência: R$ "))
    if 0 < valor <= origem[3]:
        atualizar_saldo(lista_contas, origem[0], origem[3] - valor)
        atualizar_saldo(lista_contas, destino[0], destino[3] + valor)
        print("Transferência realizada com sucesso!")
    else:
        print("Saldo insuficiente ou valor inválido.")


def consultar_saldo(lista_contas):
    c = procurar_conta(lista_contas, input("Número da Conta: "))
    print(
        f"Saldo da Conta {c[0]}: R$ {c[3]:.2f}"
        if c
        else "Conta não encontrada!"
    )


def listar_contas(lista_contas):
    if not lista_contas:
        return print("Nenhuma conta cadastrada.")
    for c in lista_contas:
        print(
            f"Conta: {c[0]} | CPF: {c[1]} | Agência: {c[2]} | Saldo: R$ {c[3]:.2f}"
        )


def calcular_montante_agencia(lista_contas, codigo_agencia):
    montante_total = 0.0
    for conta in lista_contas:
        if conta[2] == codigo_agencia:
            montante_total += conta[3]  
    return montante_total


def calcular_montante_banco(lista_contas):
    montante_total = 0.0
    for conta in lista_contas:
        montante_total += conta[3] 
    return montante_total



# Implementando o metodo de selvamento em JSON
def salvar_dados_json(lista_clientes, lista_agencias, lista_contas):
    dados = {
        "clientes": lista_clientes,
        "agencias": lista_agencias,
        "contas": lista_contas,
    }
    with open("banco_dados.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)


def carregar_dados_json(lista_clientes, lista_agencias, lista_contas):
    try:
        with open("banco_dados.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            lista_clientes.extend(tuple(c) for c in dados.get("clientes", []))
            lista_agencias.extend(tuple(a) for a in dados.get("agencias", []))
            lista_contas.extend(tuple(c) for c in dados.get("contas", []))
    except FileNotFoundError:
        pass