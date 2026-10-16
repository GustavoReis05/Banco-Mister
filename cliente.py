from datetime import date

CAMPOS_CLIENTE = ("cpf", "nome", "data_nascimento", "numero_telefone")
CARACTERES_CPF = set("0123456789.-")


def primeiro(predicado, lista):
    """Função de ordem superior: retorna o 1º item que satisfaz o predicado, ou None."""
    return next(filter(predicado, lista), None)


def normalizar(texto):
    return str(texto).strip().lower()


def somente_digitos(texto):
    """Remove tudo que não for número."""
    return "".join(filter(str.isdigit, str(texto)))


def digito_verificador(numeros, posicao):
    """Calcula o dígito verificador da posição 9 (1º) ou 10 (2º)."""
    pesos = range(posicao + 1, 1, -1)
    soma = sum(int(n) * peso for n, peso in zip(numeros[:posicao], pesos))
    return (soma * 10 % 11) % 10


def validar_cpf(cpf):
    """Retorna True se o CPF for válido (formato e dígitos verificadores)."""
    if not all(ch in CARACTERES_CPF for ch in cpf):
        return False

    numeros = somente_digitos(cpf)

    # Precisa ter 11 dígitos e não pode ser sequência repetida (111.111.111-11)
    if len(numeros) != 11 or numeros == numeros[0] * 11:
        return False

    return all(digito_verificador(numeros, p) == int(numeros[p]) for p in (9, 10))


def formatar_cpf(cpf):
    """Formata 12345678909 como 123.456.789-09."""
    n = somente_digitos(cpf)
    return f"{n[:3]}.{n[3:6]}.{n[6:9]}-{n[9:]}"


def cadastrar_cliente(lista_clientes, cpf, nome, data_nascimento, numero_telefone):
    cpf, nome, data_nascimento, numero_telefone = map(
        str.strip, (cpf, nome, data_nascimento, numero_telefone)
    )

    if not all((cpf, nome, data_nascimento, numero_telefone)):
        raise ValueError("Preencha todos os campos do cliente.")

    if not validar_cpf(cpf):
        raise ValueError("CPF inválido.")

    cpf_digitos = somente_digitos(cpf)
    if any(somente_digitos(c["cpf"]) == cpf_digitos for c in lista_clientes):
        raise ValueError("Já existe um cliente com esse CPF.")

    try:
        nascimento = date.fromisoformat(data_nascimento)
    except ValueError:
        raise ValueError("Data de nascimento inválida.")

    if nascimento > date.today():
        raise ValueError("A data de nascimento não pode estar no futuro.")

    valores = (formatar_cpf(cpf), nome, data_nascimento, numero_telefone)
    return {campo: valor for campo, valor in zip(CAMPOS_CLIENTE, valores)}


def procurar_cliente(lista_clientes, termo_busca, exibir=True):
    """Busca um cliente pelo CPF ou nome (ignora maiúsculas e pontuação do CPF)."""
    termo = normalizar(termo_busca)
    if not termo:
        return None

    termo_cpf = termo.replace(".", "").replace("-", "")

    # 1) Correspondência exata de CPF ou nome
    exato = primeiro(
        lambda c: str(c.get("cpf", "")).replace(".", "").replace("-", "") == termo_cpf
        or normalizar(c.get("nome", "")) == termo,
        lista_clientes,
    )
    if exato:
        return exato

    # 2) Trecho do nome, só se houver exatamente um cliente que combine
    candidatos = [c for c in lista_clientes if termo in normalizar(c.get("nome", ""))]
    if len(candidatos) == 1:
        return candidatos[0]
    if len(candidatos) > 1 and exibir:
        print("Mais de um cliente com esse nome. Digite o nome completo ou o CPF.")
    return None


def listar_clientes(lista_clientes, filtro=lambda cliente: True):
    """Retorna os clientes cadastrados, opcionalmente filtrados por uma função."""
    return [cliente for cliente in lista_clientes if filtro(cliente)]
