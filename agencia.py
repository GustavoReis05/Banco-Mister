def cadastrar_agencia():
    """Solicita os dados da agência e retorna uma tupla."""
    codigo = input("Código da Agência: \n")
    nome = input("Nome da Agência: \n")
    cidade_e_estado = input("Cidade e Estado onde a Agência é Localizada: \n")

    agencia = (codigo, nome, cidade_e_estado)
    print("AGÊNCIA CADASTRADA COM SUCESSO!")
    return agencia

def procurar_agencia(lista_agencias, codigo):
    '''Consulta se uma agencia está contida na lista de agencias'''
    for agencia in lista_agencias:
        if agencia[0] == codigo:
            return agencia


def listar_agencias(lista_agencias):
    """Exibe todas as agências cadastradas."""
    if not lista_agencias:
        print("Nenhuma agência cadastrada.")
        return

    print("--- LISTA DE AGÊNCIAS ---")
    for agencia in lista_agencias:
            print(agencia[0], agencia[1])
