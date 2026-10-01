import json
from agencia import procurar_agencia
from cliente import procurar_cliente

# Estrutura da Tupla: (numero_conta, cpf_cliente, codigo_agencia, saldo, tipo)

TIPOS_CONTA = {
    "1": "poupança",
    "2": "corrente",
    "3": "salário",
}

# A poupança está rendendo a Taxa Selic, que está a 13,75% ao ano
TAXA_ANUAL_POUPANCA = 0.1375


# Seleção do tipo de conta (Salário, Poupança, Corrente)
def escolher_tipo_conta():
    while True:
        print("\nTipo de conta:")
        for codigo, nome in TIPOS_CONTA.items():
            print(f"  {codigo} - {nome.capitalize()}")

        opcao = input("Escolha o tipo: ").strip()
        if opcao in TIPOS_CONTA:
            return TIPOS_CONTA[opcao]
        print("Opção inválida! Tente novamente.")


# Função de cadastro de conta. Dados lidos
'''Essa função consulta se o cliente e a aencia já estão cadastrados. 
Se estiverem cadastrados, ela lê o numero da conta e o tipo'''
def cadastrar_conta(lista_clientes, lista_agencias):
    termo_busca = input("CPF ou Nome do cliente: ").strip().lower()
    cliente_encontrado = procurar_cliente(lista_clientes, termo_busca)

    if not cliente_encontrado:
        print("Cliente não encontrado!")
        return None

    cpf = cliente_encontrado['cpf']

    agencia_cod = input("Código da agência: ")
    if not procurar_agencia(lista_agencias, agencia_cod):
        print("Agência não encontrada!")
        return None

    numero_conta = input("Digite o numero da conta: ")
    tipo_conta = escolher_tipo_conta()

    print(f"Conta {tipo_conta} - {numero_conta} criada com sucesso!")
    return {'numero_conta': numero_conta, 'cpf': cpf, 'agencia_cod': agencia_cod, 'saldo_conta': 0.0, 'tipo': tipo_conta}


def procurar_conta(lista_contas, numero):
    for c in lista_contas:
        if c['numero_conta'] == numero:
            return c
    return None


def atualizar_saldo(lista_contas, numero, novo_saldo):
    for i, c in enumerate(lista_contas):
        if c['numero_conta'] == numero:
            lista_contas[i] = (c[0], c[1], c[2], novo_saldo, *c[4:])
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


def aplicar_rendimento(lista_contas):
    entrada = input("Quantos meses de rendimento? (Enter = 12 meses, 13,75% cheio): ").strip()

    if entrada == "":
        meses = 12
    else:
        try:
            meses = int(entrada)
        except ValueError:
            return print("Digite um número inteiro de meses.")

    if meses <= 0:
        return print("O número de meses deve ser maior que zero.")

    fator = (1 + TAXA_ANUAL_POUPANCA) ** (meses / 12)
    contas_atualizadas = 0

    for i, c in enumerate(lista_contas):
        tipo = c[4] if len(c) > 4 else None

        if tipo != "poupança":
            print(f"Conta {c[0]}: ignorada (tipo: {tipo or 'não informado'}).")
            continue

        saldo_antigo = c[3]
        novo_saldo = round(saldo_antigo * fator, 2)
        lista_contas[i] = (c[0], c[1], c[2], novo_saldo, *c[4:])
        contas_atualizadas += 1
        print(
            f"Conta {c[0]}: R$ {saldo_antigo:.2f} -> R$ {novo_saldo:.2f} "
            f"(+R$ {novo_saldo - saldo_antigo:.2f})"
        )

    print(
        f"\nRendimento de {meses} mês(es) aplicado em "
        f"{contas_atualizadas} conta(s) poupança."
    )


def listar_contas(lista_contas):
    if not lista_contas:
        return print("Nenhuma conta cadastrada.")
    for c in lista_contas:
        tipo = c[4] if len(c) > 4 else "não informado"
        print(
            f"Conta: {c[0]} | {tipo.capitalize()} | CPF: {c[1]} | "
            f"Agência: {c[2]} | Saldo: R$ {c[3]:.2f}"
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


# Implementando o metodo de salvamento em JSON
def salvar_dados_json(lista_clientes, lista_agencias, lista_contas):
    dados = {
        "clientes": lista_clientes,
        "agencias": lista_agencias,
        "contas": lista_contas,
    }
    with open("banco_dados.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def carregar_dados_json(lista_clientes, lista_agencias, lista_contas):
    try:
        with open("banco_dados.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            # Agora ele carrega a lista de dicionários diretamente
            lista_clientes.extend(dados.get("clientes", []))
            lista_agencias.extend(dados.get("agencias", []))
            lista_contas.extend(dados.get("contas", []))
    except FileNotFoundError:
        pass