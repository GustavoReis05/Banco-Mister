
import math
from agencia import Agencia
from cliente import Cliente


class Conta:

    TIPOS_CONTA = {
        "1": "poupança",
        "2": "corrente",
    }

    OPERACOES_PERMITIDAS = {
        "poupança": {"sacar", "depositar", "transferir"},
        "corrente": {"sacar", "depositar", "transferir"},
        "salário": {"sacar", "depositar"},
    }

    def __init__(self, numero_conta, cpf, agencia_cod, tipo, saldo_conta=0.0):

        self.numero_conta = str(numero_conta).strip()
        self.cpf = str(cpf).strip()
        self.agencia_cod = str(agencia_cod).strip()
        self.tipo = str(tipo).strip()
        self.saldo_conta = float(saldo_conta)

        if not all((
            self.numero_conta,
            self.cpf,
            self.agencia_cod,
            self.tipo
        )):
            raise ValueError("Preencha todos os campos da conta.")

        if self.tipo not in self.TIPOS_CONTA.values():
            raise ValueError("Tipo de conta inválido.")

        if not math.isfinite(self.saldo_conta) or self.saldo_conta < 0:
            raise ValueError("Saldo inicial inválido.")

    # ---------- Cadastro ----------

    @staticmethod
    def cadastrar(
        lista_clientes,
        lista_agencias,
        lista_contas,
        termo_busca,
        agencia_cod,
        numero_conta,
        tipo
    ):
        """Cadastra uma nova conta."""

        termo_busca, agencia_cod, numero_conta, tipo = map(
            str.strip,
            (termo_busca, agencia_cod, numero_conta, tipo)
        )

        if not all((termo_busca, agencia_cod, numero_conta, tipo)):
            raise ValueError("Preencha todos os campos da conta.")

        cliente = Cliente.procurar(lista_clientes, termo_busca)

        if not cliente:
            raise ValueError(
                "Cliente não encontrado ou nome ambíguo. "
                "Informe o CPF ou o nome completo."
            )

        agencia = Agencia.buscar_por_codigo(lista_agencias, agencia_cod)

        if not agencia:
            raise ValueError("Agência não encontrada.")

        if Conta.buscar_por_numero(lista_contas, numero_conta):
            raise ValueError("Já existe uma conta com esse número.")

        if tipo not in Conta.TIPOS_CONTA.values():
            raise ValueError("Tipo de conta inválido.")

        nova_conta = Conta(
            numero_conta,
            cliente.cpf,
            agencia_cod,
            tipo
        )

        lista_contas.append(nova_conta)

        return nova_conta

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

    # ---------- Validações ----------

    def operacao_permitida(self, operacao):
        """Verifica se o tipo da conta permite a operação."""

        return operacao in self.OPERACOES_PERMITIDAS.get(
            self.tipo, set()
        )

    def validar_operacao(self, operacao):
        """Verifica se a conta pode realizar a operação."""

        if not self.operacao_permitida(operacao):
            raise ValueError(
                f"A conta {self.numero_conta} ({self.tipo}) "
                f"não pode realizar: {operacao}."
            )

    @staticmethod
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

    @staticmethod
    def validar_saldo_finito(saldo, mensagem):
        if not math.isfinite(saldo):
            raise ValueError(mensagem)

        return saldo

    # ---------- Operações bancárias ----------

    def sacar(self, valor):
        """Realiza um saque na conta."""

        self.validar_operacao("sacar")

        valor = self.validar_valor_operacao(valor)

        if valor > self.saldo_conta:
            raise ValueError("Saldo insuficiente.")

        self.saldo_conta = round(
            self.saldo_conta - valor, 2
        )

        return f"Saque de R$ {valor:.2f} realizado com sucesso!"

    def depositar(self, valor):
        """Realiza um depósito na conta."""

        self.validar_operacao("depositar")

        valor = self.validar_valor_operacao(valor)

        novo_saldo = self.validar_saldo_finito(
            round(self.saldo_conta + valor, 2),
            "Valor inválido para o saldo da conta."
        )

        self.saldo_conta = novo_saldo

        return f"Depósito de R$ {valor:.2f} realizado com sucesso!"

    def transferir(self, lista_contas, numero_destino, valor):
        """Transfere dinheiro para outra conta."""

        self.validar_operacao("transferir")

        destino = Conta.buscar_por_numero(
            lista_contas, numero_destino
        )

        if destino is None:
            raise ValueError("Conta de destino não encontrada!")

        if self.numero_conta == destino.numero_conta:
            raise ValueError(
                "A conta de origem e a de destino devem ser diferentes."
            )

        valor = self.validar_valor_operacao(valor)

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

