class Agencia:
    # Definiçao dos atributos da agencia
    def __init__(self, codigo_agencia, nome_agencia, cidade_estado):
        self.codigo_agencia = str(codigo_agencia).strip()
        self.nome_agencia = str(nome_agencia).strip()
        self.cidade_estado = str(cidade_estado).strip()

        if not all((
            self.codigo_agencia,
            self.nome_agencia,
            self.cidade_estado
        )):
            raise ValueError("Dados da agencia inválidos.")

    def to_dict(self):
        return {
            "codigo_agencia": self.codigo_agencia,
            "nome_agencia": self.nome_agencia,
            "cidade_estado": self.cidade_estado
        }

    @classmethod
    def from_dict(cls, dados):
        return cls(
            dados["codigo_agencia"],
            dados["nome_agencia"],
            dados["cidade_estado"]
        )

    def __str__(self):
        return (
            f"Código: {self.codigo_agencia} | "
            f"Nome: {self.nome_agencia} | "
            f"Cidade/Estado: {self.cidade_estado}"
        )
