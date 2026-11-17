
from datetime import date


class Cliente:

    def __init__(self, cpf, nome, data_nascimento, numero_telefone):

        self.cpf = self.formatar_cpf(cpf)
        self.nome = str(nome).strip()
        self.data_nascimento = str(data_nascimento).strip()
        self.numero_telefone = str(numero_telefone).strip()

        if not all((
            self.cpf,
            self.nome,
            self.data_nascimento,
            self.numero_telefone
        )):
            raise ValueError("Preencha todos os campos do cliente.")

        if not self.validar_cpf(cpf):
            raise ValueError("CPF inválido.")

        try:
            nascimento = date.fromisoformat(self.data_nascimento)
        except ValueError:
            raise ValueError("Data de nascimento inválida.")

        if nascimento > date.today():
            raise ValueError("A data de nascimento não pode estar no futuro.")

    @staticmethod
    def somente_digitos(texto):
        """Remove tudo que não for número."""
        return "".join(filter(str.isdigit, str(texto)))

    @staticmethod
    def formatar_cpf(cpf):
        """Formata o CPF."""
        n = Cliente.somente_digitos(cpf)

        if len(n) != 11:
            return str(cpf).strip()

        return f"{n[:3]}.{n[3:6]}.{n[6:9]}-{n[9:]}"

    @staticmethod
    def digito_verificador(numeros, posicao):
        """Calcula os dígitos verificadores do CPF."""
        pesos = range(posicao + 1, 1, -1)

        soma = sum(
            int(n) * peso
            for n, peso in zip(numeros[:posicao], pesos)
        )

        return (soma * 10 % 11) % 10

    @staticmethod
    def validar_cpf(cpf):
        """Verifica se o CPF é válido."""

        cpf = str(cpf).strip()

        if not all(ch in set("0123456789.-") for ch in cpf):
            return False

        numeros = Cliente.somente_digitos(cpf)

        if len(numeros) != 11 or numeros == numeros[0] * 11:
            return False

        return all(
            Cliente.digito_verificador(numeros, p) == int(numeros[p])
            for p in (9, 10)
        )

    @staticmethod
    def cadastrar(lista_clientes, cpf, nome, data_nascimento, numero_telefone):
        """Cadastra um novo cliente."""

        if not Cliente.validar_cpf(cpf):
            raise ValueError("CPF inválido.")

        cpf_digitos = Cliente.somente_digitos(cpf)

        for cliente in lista_clientes:
            if Cliente.somente_digitos(cliente.cpf) == cpf_digitos:
                raise ValueError("Já existe um cliente com esse CPF.")

        novo_cliente = Cliente(
            cpf,
            nome,
            data_nascimento,
            numero_telefone
        )

        lista_clientes.append(novo_cliente)

        return novo_cliente

    @staticmethod
    def procurar(lista_clientes, termo_busca, exibir=True):
        """Busca cliente pelo CPF ou nome."""

        termo = str(termo_busca).strip().lower()

        if not termo:
            return None

        termo_cpf = Cliente.somente_digitos(termo)

        # Busca exata por CPF ou nome
        for cliente in lista_clientes:

            cpf_cliente = Cliente.somente_digitos(cliente.cpf)

            if cpf_cliente == termo_cpf or cliente.nome.lower() == termo:
                return cliente

        # Busca por parte do nome
        candidatos = [
            cliente for cliente in lista_clientes
            if termo in cliente.nome.lower()
        ]

        if len(candidatos) == 1:
            return candidatos[0]

        if len(candidatos) > 1 and exibir:
            print(
                "Mais de um cliente com esse nome. "
                "Digite o nome completo ou o CPF."
            )

        return None

    @staticmethod
    def listar(lista_clientes, filtro=None):
        """Lista os clientes, permitindo aplicar filtros."""

        if filtro is None:
            return lista_clientes

        return [
            cliente for cliente in lista_clientes
            if filtro(cliente)
        ]

    def __str__(self):
        return (
            f"CPF: {self.cpf} | "
            f"Nome: {self.nome} | "
            f"Data de nascimento: {self.data_nascimento} | "
            f"Telefone: {self.numero_telefone}"
        )