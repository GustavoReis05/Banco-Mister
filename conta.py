import json
from agencia import procurar_agencia
from cliente import procurar_cliente

# Estrutura da conta (dicionário):
# {'numero_conta', 'cpf', 'agencia_cod', 'saldo_conta', 'tipo'}

TIPOS_CONTA = {
    "1": "poupança",
    "2": "corrente",
    "3": "salário",
}

# Operações permitidas para cada tipo de conta
OPERACOES_PERMITIDAS = {
    "poupança": {"sacar", "depositar", "transferir"},
    "corrente": {"sacar", "depositar", "transferir"},
    "salário": {"sacar", "depositar"},  # salário não pode transferir
}

# A poupança está rendendo a Taxa Selic, que está a 13,75% ao ano
TAXA_ANUAL_POUPANCA = 0.1375


def operacao_permitida(conta, operacao):
    """Verifica se o tipo da conta permite a operação."""
    tipo = conta.get("tipo")
    if operacao in OPERACOES_PERMITIDAS.get(tipo, set()):
        return True
    print(f"A conta {conta['numero_conta']} ({tipo}) não pode realizar: {operacao}.")
    return False


def ler_valor(mensagem):
    """Lê um valor em reais. Retorna None se for inválido."""
    try:
        return float(input(mensagem).replace(",", "."))
    except ValueError:
        print("Valor inválido! Digite apenas números.")
        return None


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


# Função de cadastro de conta.
# Consulta se o cliente e a agência já estão cadastrados.
# Se estiverem, lê o número da conta e o tipo.
def cadastrar_conta(lista_clientes, lista_agencias, lista_contas):
    termo_busca = input("CPF ou Nome do cliente: ").strip().lower()
    cliente_encontrado = procurar_cliente(lista_clientes, termo_busca)

    if not cliente_encontrado:
        print("Cliente não encontrado!")
        return None

    cpf = cliente_encontrado["cpf"]

    agencia_cod = input("Código da agência: ").strip()
    if not procurar_agencia(lista_agencias, agencia_cod):
        print("Agência não encontrada!")
        return None

    numero_conta = input("Digite o numero da conta: ").strip()
    if procurar_conta(lista_contas, numero_conta):
        print("Erro: Já existe uma conta com esse número!")
        return None   
    
    tipo_conta = escolher_tipo_conta()

    print(f"Conta {tipo_conta} - {numero_conta} criada com sucesso!")
    return {
        "numero_conta": numero_conta,
        "cpf": cpf,
        "agencia_cod": agencia_cod,
        "saldo_conta": 0.0,
        "tipo": tipo_conta,
    }


def procurar_conta(lista_contas, numero):
    for c in lista_contas:
        if c["numero_conta"] == numero:
            return c
    return None


def atualizar_saldo(lista_contas, numero, novo_saldo):
    for conta in lista_contas:
        if conta["numero_conta"] == numero:
            conta["saldo_conta"] = novo_saldo
            break


def sacar(lista_contas):
    c = procurar_conta(lista_contas, input("Número da Conta: ").strip())
    if not c:
        return print("Conta não encontrada!")
    if not operacao_permitida(c, "sacar"):
        return

    valor = ler_valor("Valor do saque: R$ ")
    if valor is None:
        return

    if 0 < valor <= c["saldo_conta"]:
        atualizar_saldo(lista_contas, c["numero_conta"], c["saldo_conta"] - valor)
        print(f"Saque de R$ {valor:.2f} realizado!")
    else:
        print("Valor inválido ou saldo insuficiente.")


def depositar(lista_contas):
    c = procurar_conta(lista_contas, input("Número da Conta: ").strip())
    if not c:
        return print("Conta não encontrada!")
    if not operacao_permitida(c, "depositar"):
        return

    valor = ler_valor("Valor do depósito: R$ ")
    if valor is None:
        return

    if valor > 0:
        atualizar_saldo(lista_contas, c["numero_conta"], c["saldo_conta"] + valor)
        print(f"Depósito de R$ {valor:.2f} realizado!")
    else:
        print("Valor inválido.")


def transferir(lista_contas):
    origem = procurar_conta(lista_contas, input("Número da Conta Origem: ").strip())
    if not origem:
        return print("Conta de origem não encontrada!")
    if not operacao_permitida(origem, "transferir"):
        return

    destino = procurar_conta(lista_contas, input("Número da Conta Destino: ").strip())
    if not destino:
        return print("Conta de destino não encontrada!")
    if origem["numero_conta"] == destino["numero_conta"]:
        return print("A conta de origem e a de destino devem ser diferentes.")

    valor = ler_valor("Valor da transferência: R$ ")
    if valor is None:
        return

    if 0 < valor <= origem["saldo_conta"]:
        atualizar_saldo(lista_contas, origem["numero_conta"], origem["saldo_conta"] - valor)
        atualizar_saldo(lista_contas, destino["numero_conta"], destino["saldo_conta"] + valor)
        print("Transferência realizada com sucesso!")
    else:
        print("Saldo insuficiente ou valor inválido.")


def consultar_saldo(lista_contas):
    c = procurar_conta(lista_contas, input("Número da Conta: ").strip())
    if c:
        print(f"Saldo da Conta {c['numero_conta']}: R$ {c['saldo_conta']:.2f}")
    else:
        print("Conta não encontrada!")


def aplicar_rendimento(lista_contas):
    entrada = input(
        "Quantos meses de rendimento? (Enter = 12 meses, 13,75% cheio): "
    ).strip()

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

    for c in lista_contas:
        if c.get("tipo") != "poupança":
            continue

        saldo_antigo = c["saldo_conta"]
        if saldo_antigo <= 0:
            print(f"Conta {c['numero_conta']}: saldo zerado, deposite antes para render.")
            continue

        novo_saldo = round(saldo_antigo * fator, 2)
        c["saldo_conta"] = novo_saldo
        contas_atualizadas += 1
        print(
            f"Conta {c['numero_conta']}: R$ {saldo_antigo:.2f} -> R$ {novo_saldo:.2f} "
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
        print(
            f"Conta: {c['numero_conta']} | {c['tipo'].capitalize()} | "
            f"CPF: {c['cpf']} | Agência: {c['agencia_cod']} | "
            f"Saldo: R$ {c['saldo_conta']:.2f}"
        )


def calcular_montante_agencia(lista_contas, codigo_agencia):
    montante_total = 0.0
    for conta in lista_contas:
        if conta["agencia_cod"] == codigo_agencia:
            montante_total += conta["saldo_conta"]
    return montante_total


def calcular_montante_banco(lista_contas):
    montante_total = 0.0
    for conta in lista_contas:
        montante_total += conta["saldo_conta"]
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
            lista_clientes.extend(dados.get("clientes", []))
            lista_agencias.extend(dados.get("agencias", []))
            lista_contas.extend(dados.get("contas", []))
    except FileNotFoundError:
        pass
