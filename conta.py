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


# ---------- Funções de ordem superior reutilizáveis ----------

def buscar_por(campo):
    """Recebe um campo e retorna uma função de busca por esse campo."""
    return lambda lista, valor: next(
        filter(lambda item: item[campo] == valor, lista), None
    )


def somar_saldos(contas):
    """Soma os saldos de qualquer coleção de contas."""
    return sum((conta["saldo_conta"] for conta in contas), 0.0)


procurar_conta = buscar_por("numero_conta")


def conta_por_numero(lista_contas, numero):
    """Busca a conta tolerando entrada não-string e espaços."""
    return procurar_conta(lista_contas, str(numero).strip())


# ---------- Cadastro ----------

def cadastrar_conta(
    lista_clientes,
    lista_agencias,
    lista_contas,
    termo_busca,
    agencia_cod,
    numero_conta,
    tipo,
):
    termo_busca, agencia_cod, numero_conta, tipo = map(
        str.strip, (termo_busca, agencia_cod, numero_conta, tipo)
    )

    if not all((termo_busca, agencia_cod, numero_conta, tipo)):
        raise ValueError("Preencha todos os campos da conta.")

    cliente_encontrado = procurar_cliente(lista_clientes, termo_busca)
    if not cliente_encontrado:
        raise ValueError(
            "Cliente não encontrado ou nome ambíguo. "
            "Informe o CPF ou o nome completo."
        )

    if not procurar_agencia(lista_agencias, agencia_cod):
        raise ValueError("Agência não encontrada.")

    if procurar_conta(lista_contas, numero_conta):
        raise ValueError("Já existe uma conta com esse número.")

    if tipo not in TIPOS_CONTA.values():
        raise ValueError("Tipo de conta inválido.")

    return {
        "numero_conta": numero_conta,
        "cpf": cliente_encontrado["cpf"],
        "agencia_cod": agencia_cod,
        "saldo_conta": 0.0,
        "tipo": tipo,
    }


def listar_contas(lista_contas, filtro=lambda conta: True):
    """Retorna as contas cadastradas, opcionalmente filtradas por uma função."""
    return [conta for conta in lista_contas if filtro(conta)]


# ---------- Validações ----------

def operacao_permitida(conta, operacao):
    """Verifica se o tipo da conta permite a operação."""
    return operacao in OPERACOES_PERMITIDAS.get(conta.get("tipo"), set())


def atualizar_saldo(lista_contas, numero, novo_saldo):
    """Atualiza o saldo de uma conta específica (se ela existir)."""
    conta = procurar_conta(lista_contas, numero)
    if conta:
        conta["saldo_conta"] = novo_saldo


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
    c = conta_por_numero(lista_contas, numero)
    if c is None:
        raise ValueError("Conta não encontrada!")
    if not operacao_permitida(c, operacao):
        raise ValueError(
            f"A conta {c['numero_conta']} ({c['tipo']}) não pode realizar: {operacao}."
        )
    return c


def validar_saldo_finito(saldo, mensagem):
    if not math.isfinite(saldo):
        raise ValueError(mensagem)
    return saldo


# ---------- Operações ----------

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
    novo_saldo = validar_saldo_finito(
        round(c["saldo_conta"] + valor, 2),
        "Valor inválido para o saldo da conta.",
    )
    atualizar_saldo(lista_contas, c["numero_conta"], novo_saldo)
    return f"Depósito de R$ {valor:.2f} realizado com sucesso!"


def transferir(lista_contas, numero_origem=None, numero_destino=None, valor=None):
    origem = validar_conta_operacao(lista_contas, numero_origem, "transferir")
    destino = conta_por_numero(lista_contas, numero_destino)
    if destino is None:
        raise ValueError("Conta de destino não encontrada!")
    if origem["numero_conta"] == destino["numero_conta"]:
        raise ValueError("A conta de origem e a de destino devem ser diferentes.")
    valor = validar_valor_operacao(valor)
    if valor > origem["saldo_conta"]:
        raise ValueError("Saldo insuficiente.")
    saldo_destino = validar_saldo_finito(
        round(destino["saldo_conta"] + valor, 2),
        "Valor inválido para o saldo da conta de destino.",
    )
    atualizar_saldo(lista_contas, origem["numero_conta"], round(origem["saldo_conta"] - valor, 2))
    atualizar_saldo(lista_contas, destino["numero_conta"], saldo_destino)
    return "Transferência realizada com sucesso!"


def consultar_saldo(lista_contas):
    c = conta_por_numero(lista_contas, input("Número da Conta: "))
    if c:
        print(f"Saldo da Conta {c['numero_conta']}: R$ {c['saldo_conta']:.2f}")
    else:
        print("Conta não encontrada!")


# ---------- Rendimento da poupança ----------

def render_conta(conta, fator):
    """Aplica o fator à conta. Retorna (atualizada, mensagem)."""
    saldo_antigo = conta["saldo_conta"]
    if saldo_antigo <= 0:
        return False, f"Conta {conta['numero_conta']}: saldo zerado, deposite antes para render."

    novo_saldo = round(saldo_antigo * fator, 2)
    conta["saldo_conta"]
