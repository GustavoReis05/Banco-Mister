from functools import partial

import agencia
import cliente
import conta

lista_clientes = []
lista_agencias = []
lista_contas = []

OPCOES_MENU = [
    ("1", "Cadastrar Cliente"),
    ("2", "Cadastrar Agência"),
    ("3", "Cadastrar Conta"),
    ("4", "Buscar Cliente"),
    ("5", "Listar Clientes"),
    ("6", "Listar Agências"),
    ("7", "Listar Contas"),
    ("8", "Sacar"),
    ("9", "Depositar"),
    ("10", "Transferir"),
    ("11", "Consultar Saldo"),
    ("12", "Relatório: Montante Total da Agência"),
    ("13", "Relatório: Montante Total do Banco"),
    ("14", "Aplicar Rendimento da Poupança"),
    ("0", "Sair e Salvar"),
]


# ---------- Funções de ordem superior que geram os handlers do menu ----------

def cadastrar_em(lista_destino, cadastrar, *listas_entrada, mensagem=None):
    """Retorna um handler que chama `cadastrar(*listas_entrada)` e,
    se devolver algo, adiciona o resultado em `lista_destino`."""
    def executar():
        novo = cadastrar(*listas_entrada)
        if novo:
            lista_destino.append(novo)
            if mensagem:
                print(mensagem)
    return executar


def listar(lista, titulo, mensagem_vazia, formatar):
    """Retorna um handler que imprime `lista` numerada, usando `formatar` em cada item."""
    def executar():
        if not lista:
            print(f"\n{mensagem_vazia}")
            return
        print(f"\n=== {titulo} ===")
        print("\n".join(
            [f"{i}. {formatar(item)}" for i, item in enumerate(lista, start=1)]
        ))
    return executar


# ---------- Handlers específicos ----------

def buscar_cliente():
    termo_busca = input("Digite o CPF ou Nome do cliente: ").strip()
    cliente_encontrado = cliente.procurar_cliente(lista_clientes, termo_busca)

    if not cliente_encontrado:
        print("Cliente não encontrado!")
        return

    campos = [
        ("CPF", "cpf"),
        ("Nome", "nome"),
        ("Data de Nascimento", "data_nascimento"),
        ("Telefone", "numero_telefone"),
    ]
    print("\n=== CLIENTE ENCONTRADO ===")
    print("\n".join(
        [f"{rotulo}: {cliente_encontrado[chave]}" for rotulo, chave in campos]
    ))


def montante_agencia():
    codigo = input("Digite o código da agência: ").strip()
    agencia_encontrada = agencia.procurar_agencia(lista_agencias, codigo)

    if not agencia_encontrada:
        print("Agência não encontrada.")
        return

    total = conta.calcular_montante_agencia(lista_contas, codigo)
    print(
        f"Montante Total na Agência {agencia_encontrada['codigo_agencia']} "
        f"({agencia_encontrada['nome_agencia']}): R$ {total:.2f}"
    )


def montante_banco():
    total_banco = conta.calcular_montante_banco(lista_contas)
    print(f"Montante Total no Banco Mister: R$ {total_banco:.2f}")


def salvar_dados():
    conta.salvar_dados_json(lista_clientes, lista_agencias, lista_contas)
    print("Dados salvos em banco_dados.json com sucesso!")
    print("Saindo do programa...")


# ---------- Tabela de ações: opção -> função sem argumentos ----------

ACOES = {
    "1": cadastrar_em(
        lista_clientes, cliente.cadastrar_cliente, lista_clientes,
        mensagem="Cliente adicionado à memória.",
    ),
    "2": cadastrar_em(
        lista_agencias, agencia.cadastrar_agencia, lista_agencias,
        mensagem="Agência adicionada à memória.",
    ),
    "3": cadastrar_em(
        lista_contas, conta.cadastrar_conta,
        lista_clientes, lista_agencias, lista_contas,
    ),
    "4": buscar_cliente,
    "5": listar(
        lista_clientes, "LISTA DE CLIENTES", "Nenhum cliente cadastrado.",
        lambda c: f"CPF: {c['cpf']} | Nome: {c['nome']} | Tel: {c['numero_telefone']}",
    ),
    "6": listar(
        lista_agencias, "LISTA DE AGÊNCIAS", "Nenhuma agência cadastrada.",
        lambda a: f"Código: {a['codigo_agencia']} | Nome: {a['nome_agencia']}",
    ),
    "7": partial(conta.listar_contas, lista_contas),
    "8": partial(conta.sacar, lista_contas),
    "9": partial(conta.depositar, lista_contas),
    "10": partial(conta.transferir, lista_contas),
    "11": partial(conta.consultar_saldo, lista_contas),
    "12": montante_agencia,
    "13": montante_banco,
    "14": partial(conta.aplicar_rendimento, lista_contas),
}


def exibir_menu():
    print("\n=== BANCO MISTER ===")
    print("\n".join([f"{codigo} - {texto}" for codigo, texto in OPCOES_MENU]))


def menu_principal():
    conta.carregar_dados_json(lista_clientes, lista_agencias, lista_contas)

    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "0":
            salvar_dados()
            break

        acao = ACOES.get(opcao)
        if acao:
            acao()
        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    menu_principal()
