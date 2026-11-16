class Agencia:
    def __init__(self, codigo_agencia, nome_agencia, cidade_estado):
        self.codigo_agencia = str(codigo_agencia).strip()
        self.nome_agencia = str(nome_agencia).strip()
        self.cidade_estado = str(cidade_estado).strip()

        if not all((self.codigo_agencia, self.nome_agencia, self.cidade_estado)):
            raise ValueError("Preencha todos os campos da agência.")

    @staticmethod
    def buscar_por_codigo(lista_agencias, codigo):
        """Busca uma agência pelo código."""
        codigo = str(codigo).strip()
        for agencia in lista_agencias:
            if agencia.codigo_agencia == codigo:
                return agencia
        return None

    @staticmethod
    def cadastrar(lista_agencias, codigo, nome, cidade_estado):
        """Cadastra uma nova agência."""
        if Agencia.buscar_por_codigo(lista_agencias, codigo):
            raise ValueError("Já existe uma agência com esse código.")

        nova_agencia = Agencia(codigo, nome, cidade_estado)
        lista_agencias.append(nova_agencia)
        return nova_agencia

    @staticmethod
    def listar(lista_agencias, filtro=None):
        """Lista as agências, permitindo aplicar um filtro."""
        if filtro is None:
            return lista_agencias
        return [agencia for agencia in lista_agencias if filtro(agencia)]

    def __str__(self):
        return (
            f"Código: {self.codigo_agencia} | "
            f"Nome: {self.nome_agencia} | "
            f"Cidade/Estado: {self.cidade_estado}"
        )
