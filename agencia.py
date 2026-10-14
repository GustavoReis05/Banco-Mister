def cadastrar_agencia(lista_agencias, codigo, nome, cidade_estado):
    codigo = codigo.strip()
    nome = nome.strip()
    cidade_estado = cidade_estado.strip()

    if not all([codigo, nome, cidade_estado]):
        raise ValueError("Preencha todos os campos da agência.")

    if procurar_agencia(lista_agencias, codigo):
        raise ValueError("Já existe uma agência com esse código.")

    return {
        "codigo_agencia": codigo,
        "nome_agencia": nome,
        "cidade_estado": cidade_estado,
    }

def procurar_agencia(lista_agencias, codigo):
    """Consulta se uma agência está contida na lista de agências."""
    for agencia in lista_agencias:
        if agencia["codigo_agencia"] == codigo:
            return agencia
    return None


def listar_agencias(lista_agencias):
    """Exibe todas as agências cadastradas."""
    if not lista_agencias:
        print("Nenhuma agência cadastrada.")
        return

    print("--- LISTA DE AGÊNCIAS ---")
    for agencia in lista_agencias:
        print(agencia["codigo_agencia"], agencia["nome_agencia"])
