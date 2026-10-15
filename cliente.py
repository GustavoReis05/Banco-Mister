from datetime import date

def somente_digitos(texto):
    """Remove tudo que não for número."""
    return "".join(ch for ch in str(texto) if ch.isdigit())


def validar_cpf(cpf):
    """Retorna True se o CPF for válido (formato e dígitos verificadores)."""
    # Aceita apenas números, pontos e traço
    if any(ch not in "0123456789.-" for ch in cpf):
        return False

    numeros = somente_digitos(cpf)

    # Precisa ter 11 dígitos e não pode ser sequência repetida (111.111.111-11)
    if len(numeros) != 11 or numeros == numeros[0] * 11:
        return False

    # Calcula o 1º e o 2º dígito verificador
    for posicao in (9, 10):
        soma = sum(int(numeros[j]) * (posicao + 1 - j) for j in range(posicao))
        digito = (soma * 10 % 11) % 10
        if digito != int(numeros[posicao]):
            return False

    return True


def formatar_cpf(cpf):
    """Formata 12345678909 como 123.456.789-09."""
    n = somente_digitos(cpf)
    return f"{n[:3]}.{n[3:6]}.{n[6:9]}-{n[9:]}"


def ler_cpf(lista_clientes=None):
    """Pede o CPF até ser válido (e, se a lista for passada, ainda não cadastrado)."""
    while True:
        cpf = input("CPF: \n").strip()

        if not validar_cpf(cpf):
            print("CPF inválido! Digite 11 números (com ou sem pontos e traço).")
            continue

        if lista_clientes is not None:
            numeros = somente_digitos(cpf)
            if any(somente_digitos(c.get("cpf", "")) == numeros for c in lista_clientes):
                print("Já existe um cliente cadastrado com esse CPF!")
                continue

        return formatar_cpf(cpf)


def cadastrar_cliente(
    lista_clientes,
    cpf,
    nome,
    data_nascimento,
    numero_telefone,
):
    cpf = cpf.strip()
    nome = nome.strip()
    data_nascimento = data_nascimento.strip()
    numero_telefone = numero_telefone.strip()

    # Verifica os campos obrigatórios.
    if not all([cpf, nome, data_nascimento, numero_telefone]):
        raise ValueError("Preencha todos os campos do cliente.")

    # Usa a função de validação que já existe neste arquivo.
    if not validar_cpf(cpf):
        raise ValueError("CPF inválido.")

    # Impede o cadastro de um CPF já existente.
    for cliente_existente in lista_clientes:
        cpf_existente = somente_digitos(cliente_existente["cpf"])

        if cpf_existente == somente_digitos(cpf):
            raise ValueError("Já existe um cliente com esse CPF.")

    # Verifica a data recebida do formulário.
    try:
        nascimento = date.fromisoformat(data_nascimento)
    except ValueError:
        raise ValueError("Data de nascimento inválida.")

    if nascimento > date.today():
        raise ValueError("A data de nascimento não pode estar no futuro.")

    # Devolve o cliente criado.
    return {
        "cpf": formatar_cpf(cpf),
        "nome": nome,
        "data_nascimento": data_nascimento,
        "numero_telefone": numero_telefone,
    }


def procurar_cliente(lista_clientes, termo_busca):
    """Busca um cliente pelo CPF ou nome (ignora maiúsculas e pontuação do CPF)"""
    termo = termo_busca.strip().lower()
    termo_cpf = termo.replace(".", "").replace("-", "")

    if not termo:
        return None

    # 1) Correspondência exata de CPF ou nome
    for cliente in lista_clientes:
        cpf = str(cliente.get("cpf", "")).replace(".", "").replace("-", "")
        nome = str(cliente.get("nome", "")).strip().lower()
        if cpf == termo_cpf or nome == termo:
            return cliente

    # 2) Trecho do nome, só se houver exatamente um cliente que combine
    candidatos = [
        c for c in lista_clientes
        if termo in str(c.get("nome", "")).strip().lower()
    ]
    if len(candidatos) == 1:
        return candidatos[0]
    if len(candidatos) > 1:
        print("Mais de um cliente com esse nome. Digite o nome completo ou o CPF.")
    return None


def listar_clientes(lista_clientes, exibir=True):
    """Retorna ou exibe a lista de clientes."""
    if exibir:
        if not lista_clientes:
            print("\nNenhum cliente cadastrado.")
        else:
            print("\n=== LISTA DE CLIENTES ===")
            for i, c in enumerate(lista_clientes, start=1):
                print(f"{i}. CPF: {c['cpf']} | Nome: {c['nome']} | Tel: {c['numero_telefone']}")
    return lista_clientes
