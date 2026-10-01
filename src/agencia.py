def cadastrar_agencia():
    """Solicita os dados da agência e retorna um dicionário."""
    codigo = input("Código da Agência: \n").strip()
    nome = input("Nome da Agência: \n")
    cidade_e_estado = input("Cidade e Estado onde a Agência é Localizada: \n")

    print("AGÊNCIA CADASTRADA COM SUCESSO!")
    return {
        "codigo_agencia": codigo,
        "nome_agencia": nome,
        "cidade_estado": cidade_e_estado,
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
