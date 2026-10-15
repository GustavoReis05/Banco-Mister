import math
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


# Função de cadastro de conta.
# Consulta se o cliente e a agência já estão cadastrados.
def cadastrar_conta(
    lista_clientes,
    lista_agencias,
    lista_contas,
    termo_busca,
    agencia_cod,
    numero_conta,
    tipo,
):
    termo_busca = termo_busca.strip()
    agencia_cod = agencia_cod.strip()
    numero_conta = numero_conta.strip()
    tipo = tipo.strip()

    # Verifica os campos obrigatórios
    if not all([termo_busca, agencia_cod, numero_conta, tipo]):
        raise ValueError("Preencha todos os campos da conta.")

    # Procura o cliente pelo CPF ou nome
    cliente_encontrado = procurar_cliente(
        lista_clientes,
        termo_busca,
    )

    if not cliente_encontrado:
        raise ValueError(
            "Cliente não encontrado ou nome ambíguo. "
            "Informe o CPF ou o nome completo."
        )

    # Confirma se a agência existe
    if not procurar_agencia(lista_agencias, agencia_cod):
        raise ValueError("Agência não encontrada.")

    # Verifica se o numero da conta esta duplicado 
    if procurar_conta(lista_contas, numero_conta):
        raise ValueError("Já existe uma conta com esse número.")

    # Confirma o tipo de conta
    if tipo not in TIPOS_CONTA.values():
        raise ValueError("Tipo de conta inválido.")

    # Devolve a conta 
    return {
        "numero_conta": numero_conta,
        "cpf": cliente_encontrado["cpf"],
        "agencia_cod": agencia_cod,
        "saldo_conta": 0.0,
        "tipo": tipo,
    }

# Busca a conta na lista de contas
def procurar_conta(lista_contas, numero):
    for c in lista_contas:
        if c["numero_conta"] == numero:
            return c
    return None


def listar_contas(lista_contas):
    """Retorna todas as contas cadastradas."""
    return lista_contas


def operacao_permitida(conta, operacao):
    """Verifica se o tipo da conta permite a operação."""
    return operacao in OPERACOES_PERMITIDAS.get(conta.get("tipo"), set())


# Função generica que atualiza o saldo de uma conta especifica
def atualizar_saldo(lista_contas, numero, novo_saldo):
    for conta in lista_contas:
        if conta["numero_conta"] == numero:
            conta["saldo_conta"] = novo_saldo
            break


def validar_valor_operacao(valor):
    """Converte reais com ponto ou vírgula e rejeita valores inválidos."""
    try:
        valor = float(str(valor).strip().replace(",", "."))
    except (TypeError, ValueError):
        raise ValueError("Valor inválido! Digite apenas números.")
    if not math.isfinite(valor) or valor <= 0:
        raise ValueError("O valor deve ser finito e maior que zero.")
    if round(valor, 2) != valor:
        raise ValueError("Informe um valor com no máximo duas casas decimais.")
    return valor



def validar_conta_operacao(lista_contas, numero, operacao):
    c = procurar_conta(lista_contas, str(numero).strip())
    if c is None:
        raise ValueError("Conta não encontrada!")
    if not operacao_permitida(c, operacao):
        raise ValueError(
            f"A conta {c['numero_conta']} ({c['tipo']}) não pode realizar: {operacao}."
        )
    return c


def sacar(lista_contas, numero=None, valor=None):
    c = validar_conta_operacao(lista_contas, numero, "sacar")
    valor = validar_valor_operacao(valor)
    if valor > c["saldo_conta"]:
        raise ValueError("Saldo insuficiente.")
    atualizar_saldo(lista_contas, c["numero_conta"], round(c["saldo_conta"] - valor, 2))
    return f"Saque de R$ {valor:.2f} realizado com sucesso!"


def depositar(lista_contas, numero=None, valor=None):
    c = validar_conta_operacao(lista_contas, numero, "depositar")
    valor = validar_valor_operacao(valor)
    novo_saldo = round(c["saldo_conta"] + valor, 2)
    if not math.isfinite(novo_saldo):
        raise ValueError("Valor inválido para o saldo da conta.")
    atualizar_saldo(lista_contas, c["numero_conta"], novo_saldo)
    return f"Depósito de R$ {valor:.2f} realizado com sucesso!"


def transferir(lista_contas, numero_origem=None, numero_destino=None, valor=None):
    origem = validar_conta_operacao(lista_contas, numero_origem, "transferir")
    destino = procurar_conta(lista_contas, str(numero_destino).strip())
    if destino is None:
        raise ValueError("Conta de destino não encontrada!")
    if origem["numero_conta"] == destino["numero_conta"]:
        raise ValueError("A conta de origem e a de destino devem ser diferentes.")
    valor = validar_valor_operacao(valor)
    if valor > origem["saldo_conta"]:
        raise ValueError("Saldo insuficiente.")
    saldo_destino = round(destino["saldo_conta"] + valor, 2)
    if not math.isfinite(saldo_destino):
        raise ValueError("Valor inválido para o saldo da conta de destino.")
    atualizar_saldo(lista_contas, origem["numero_conta"], round(origem["saldo_conta"] - valor, 2))
    atualizar_saldo(lista_contas, destino["numero_conta"], saldo_destino)
    return "Transferência realizada com sucesso!"


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