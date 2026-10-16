CAMPOS_AGENCIA = ("codigo_agencia", "nome_agencia", "cidade_estado")


def buscar_por(campo):
    """Função de ordem superior: recebe um campo e retorna uma função de busca."""
    return lambda lista, valor: next(
        filter(lambda item: item[campo] == valor, lista), None
    )


procurar_agencia = buscar_por("codigo_agencia")


def cadastrar_agencia(lista_agencias, codigo, nome, cidade_estado):
    valores = list(map(str.strip, (codigo, nome, cidade_estado)))

    if not all(valores):
        raise ValueError("Preencha todos os campos da agência.")

    if procurar_agencia(lista_agencias, valores[0]):
        raise ValueError("Já existe uma agência com esse código.")

    return {campo: valor for campo, valor in zip(CAMPOS_AGENCIA, valores)}


def listar_agencias(lista_agencias, filtro=lambda agencia: True):
    """Retorna as agências cadastradas, opcionalmente filtradas por uma função."""
    return [agencia for agencia in lista_agencias if filtro(agencia)]
