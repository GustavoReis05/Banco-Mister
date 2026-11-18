import math
import unicodedata
from abc import ABC, abstractmethod


def normalizar(texto):
    texto = unicodedata.normalize(
        "NFD",
        str(texto).strip().lower()
    )

    return "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )


def validar_valor_operacao(valor):
    """Valida o valor informado para operações bancárias."""
    try:
        valor = float(
            str(valor).strip().replace(",", ".")
        )
    except (TypeError, ValueError):
        raise ValueError(
            "Valor inválido! Digite apenas números."
        )

    if not math.isfinite(valor) or valor <= 0:
        raise ValueError(
            "O valor deve ser finito e maior que zero."
        )

    if round(valor, 2) != valor:
        raise ValueError(
            "Informe um valor com no máximo duas casas decimais."
        )

    return valor


class Conta(ABC):

    TIPOS_CONTA = {
        "1": "poupança",
        "2": "corrente",
    }

    @property
    @abstractmethod
    def tipo(self):
        """Retorna o tipo da conta."""
        pass

    def __init__(self, numero_conta, cpf, agencia_cod, saldo_conta=0.0):
        self.numero_conta = str(numero_conta).strip()
        self.cpf = str(cpf).strip()
        self.agencia_cod = str(agencia_cod).strip()
        self.saldo_conta = float(saldo_conta)

        if not all((
            self.numero_conta,
            self.cpf,
            self.agencia_cod
        )):
            raise ValueError("Preencha todos os campos da conta.")

        if not math.isfinite(self.saldo_conta) or self.saldo_conta < 0:
            raise ValueError("Saldo inicial inválido.")

    @property
    def saldo(self):
        return self.saldo_conta

    @classmethod
    def criar(cls, tipo, numero_conta, agencia_cod, cpf):
        tipo_normalizado = normalizar(tipo)

        if tipo_normalizado in ("1", "poupanca"):
            return ContaPoupanca(numero_conta, cpf, agencia_cod)
        elif tipo_normalizado in ("2", "corrente"):
            return ContaCorrente(numero_conta, cpf, agencia_cod)
        else:
            raise ValueError("Tipo de conta inválido.")

    @classmethod
    def from_dict(cls, dados):
        tipo_normalizado = normalizar(dados.get("tipo", ""))
        saldo = dados.get("saldo_conta", 0.0)

        if tipo_normalizado == "poupanca":
            return ContaPoupanca(
                dados["numero_conta"],
                dados["cpf"],
                dados["agencia_cod"],
                saldo
            )
        elif tipo_normalizado == "corrente":
            return ContaCorrente(
                dados["numero_conta"],
                dados["cpf"],
                dados["agencia_cod"],
                saldo
            )
        else:
            raise ValueError("Tipo de conta inválido no banco de dados.")

    def to_dict(self):
        return {
            "numero_conta": self.numero_conta,
            "cpf": self.cpf,
            "agencia_cod": self.agencia_cod,
            "saldo_conta": self.saldo_conta,
            "tipo": self.tipo
        }

    # ---------- Busca e listagem ----------

    @staticmethod
    def buscar_por_numero(lista_contas, numero):
        """Busca uma conta pelo número."""
        numero = str(numero).strip()

        for conta in lista_contas:
            if conta.numero_conta == numero:
                return conta

        return None

    @staticmethod
    def listar(lista_contas, filtro=None):
        """Lista as contas, permitindo aplicar filtros."""
        if filtro is None:
            return lista_contas

        return [
            conta for conta in lista_contas
            if filtro(conta)
        ]

    @staticmethod
    def validar_saldo_finito(saldo, mensagem):
        if not math.isfinite(saldo):
            raise ValueError(mensagem)

        return saldo

    def validar_destino(self, destino):
        if self.numero_conta == destino.numero_conta:
            raise ValueError(
                "A conta de origem e a de destino devem ser diferentes."
            )

    # ---------- Operações bancárias ----------

    def sacar(self, valor):
        """Realiza um saque na conta."""
        valor = validar_valor_operacao(valor)

        if valor > self.saldo_conta:
            raise ValueError("Saldo insuficiente.")

        self.saldo_conta = round(
            self.saldo_conta - valor, 2
        )

        return f"Saque de R$ {valor:.2f} realizado com sucesso!"

    def depositar(self, valor):
        """Realiza um depósito na conta."""
        valor = validar_valor_operacao(valor)

        novo_saldo = self.validar_saldo_finito(
            round(self.saldo_conta + valor, 2),
            "Valor inválido para o saldo da conta."
        )

        self.saldo_conta = novo_saldo

        return f"Depósito de R$ {valor:.2f} realizado com sucesso!"

    def transferir(self, destino, valor):
        """Transfere dinheiro para outra conta."""
        self.validar_destino(destino)
        valor = validar_valor_operacao(valor)

        if valor > self.saldo_conta:
            raise ValueError("Saldo insuficiente.")

        saldo_origem = round(
            self.saldo_conta - valor, 2
        )

        saldo_destino = self.validar_saldo_finito(
            round(destino.saldo_conta + valor, 2),
            "Valor inválido para o saldo da conta de destino."
        )

        self.saldo_conta = saldo_origem
        destino.saldo_conta = saldo_destino

        return "Transferência realizada com sucesso!"

    # ---------- Cálculos e indicadores ----------

    @staticmethod
    def somar_saldos(lista_contas):
        """Soma os saldos de todas as contas."""
        return sum(
            (conta.saldo_conta for conta in lista_contas),
            0.0
        )

    @staticmethod
    def encontrar_menor_maior_saldo(lista_contas):
        """Retorna o menor e o maior saldo das contas."""
        saldos = [
            conta.saldo_conta for conta in lista_contas
        ]

        return {
            "menor_saldo": min(saldos, default=0.0),
            "maior_saldo": max(saldos, default=0.0)
        }

    @staticmethod
    def calcular_indicadores_saldos(lista_contas):
        """Calcula os indicadores para o dashboard."""
        saldos = [
            conta.saldo_conta for conta in lista_contas
        ]

        total = Conta.somar_saldos(lista_contas)

        return {
            "saldo_total": total,
            "maior_saldo": max(saldos, default=0.0),
            "saldo_medio": total / len(saldos) if saldos else 0.0
        }

    def __str__(self):
        return (
            f"Conta: {self.numero_conta} | "
            f"CPF: {self.cpf} | "
            f"Agência: {self.agencia_cod} | "
            f"Tipo: {self.tipo} | "
            f"Saldo: R$ {self.saldo_conta:.2f}"
        )


class ContaCorrente(Conta):

    def __init__(self, numero_conta, cpf, agencia_cod, saldo_conta=0.0):
        super().__init__(numero_conta, cpf, agencia_cod, saldo_conta)

    @property
    def tipo(self):
        return "corrente"


class ContaPoupanca(Conta):

    TAXA_ANUAL = 0.1375

    def __init__(self, numero_conta, cpf, agencia_cod, saldo_conta=0.0):
        super().__init__(numero_conta, cpf, agencia_cod, saldo_conta)

    @property
    def tipo(self):
        return "poupança"

    def aplicar_rendimento(self):
        self.saldo_conta = round(self.saldo_conta * (1 + self.TAXA_ANUAL), 2)