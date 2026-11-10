"""Modelos de domínio do Banco Mister (POO)."""
import math
import unicodedata
from abc import ABC
from datetime import date


def normalizar(texto):
    """minúsculas e sem acentos, para comparações."""
    texto = unicodedata.normalize("NFD", str(texto).strip().lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def apenas_digitos(texto):
    return "".join(c for c in str(texto) if c.isdigit())


CARACTERES_CPF = set("0123456789.-")


def digito_verificador(numeros, posicao):
    """Dígito verificador da posição 9 (1º) ou 10 (2º)."""
    pesos = range(posicao + 1, 1, -1)
    soma = sum(int(n) * peso for n, peso in zip(numeros[:posicao], pesos))
    return (soma * 10 % 11) % 10


def validar_cpf(cpf):
    """True se o CPF tem formato e dígitos verificadores válidos."""
    if not all(ch in CARACTERES_CPF for ch in cpf):
        return False
    numeros = apenas_digitos(cpf)
    if len(numeros) != 11 or numeros == numeros[0] * 11:
        return False
    return all(digito_verificador(numeros, p) == int(numeros[p]) for p in (9, 10))


def formatar_cpf(cpf):
    """12345678909 -> 123.456.789-09"""
    n = apenas_digitos(cpf)
    return f"{n[:3]}.{n[3:6]}.{n[6:9]}-{n[9:]}"


def validar_valor_operacao(valor):
    """Aceita ponto ou vírgula e rejeita valores inválidos."""
    try:
        valor = float(str(valor).strip().replace(",", "."))
    except (TypeError, ValueError):
        raise ValueError("Valor inválido! Digite apenas números.")
    if not math.isfinite(valor) or valor <= 0:
        raise ValueError("O valor deve ser finito e maior que zero.")
    if round(valor, 2) != valor:
        raise ValueError("Informe um valor com no máximo duas casas decimais.")
    return valor


# ---------------------------------------------------------------- Cliente

class Cliente:
    def __init__(self, cpf, nome, data_nascimento, numero_telefone):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.numero_telefone = numero_telefone

    @classmethod
    def criar(cls, cpf, nome, data_nascimento, numero_telefone):
        """Valida os dados vindos do formulário e devolve um Cliente."""
        cpf, nome, data_nascimento, numero_telefone = (
            t.strip() for t in (cpf, nome, data_nascimento, numero_telefone)
        )

        if not all((cpf, nome, data_nascimento, numero_telefone)):
            raise ValueError("Preencha todos os campos do cliente.")
        if not validar_cpf(cpf):
            raise ValueError("CPF inválido.")
        try:
            nascimento = date.fromisoformat(data_nascimento)
        except ValueError:
            raise ValueError("Data de nascimento inválida.")
        if nascimento > date.today():
            raise ValueError("A data de nascimento não pode estar no futuro.")

        return cls(formatar_cpf(cpf), nome, data_nascimento, numero_telefone)

    def corresponde_exato(self, termo):
        """CPF (ignorando . e -) ou nome completo, sem diferenciar maiúsculas."""
        termo = termo.strip().lower()
        cpf_termo = termo.replace(".", "").replace("-", "")
        cpf = self.cpf.replace(".", "").replace("-", "")
        return cpf == cpf_termo or self.nome.strip().lower() == termo

    def corresponde_parcial(self, termo):
        """Trecho do nome."""
        return termo.strip().lower() in self.nome.strip().lower()

    def to_dict(self):
        return {
            "cpf": self.cpf,
            "nome": self.nome,
            "data_nascimento": self.data_nascimento,
            "numero_telefone": self.numero_telefone,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["cpf"], d["nome"], d["data_nascimento"], d["numero_telefone"])


# ---------------------------------------------------------------- Agência

class Agencia:
    def __init__(self, codigo, nome, cidade_estado):
        self.codigo = codigo
        self.nome = nome
        self.cidade_estado = cidade_estado

    @classmethod
    def criar(cls, codigo, nome, cidade_estado):
        codigo, nome, cidade_estado = codigo.strip(), nome.strip(), cidade_estado.strip()
        if not (codigo and nome and cidade_estado):
            raise ValueError("Preencha todos os campos da agência.")
        return cls(codigo, nome, cidade_estado)

    def to_dict(self):
        return {
            "codigo_agencia": self.codigo,
            "nome_agencia": self.nome,
            "cidade_estado": self.cidade_estado,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["codigo_agencia"], d["nome_agencia"], d["cidade_estado"])


# ------------------------------------------------------------------ Conta

class Conta(ABC):
    """Classe base. Cada subclasse define seu TIPO e as operações permitidas."""

    TIPO = ""
    OPERACOES_PERMITIDAS = frozenset()
    _tipos = {}  # TIPO normalizado -> subclasse (preenchido automaticamente)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.TIPO:
            Conta._tipos[normalizar(cls.TIPO)] = cls

    def __init__(self, numero_conta, agencia_cod, cpf, saldo_conta=0.0):
        self.numero_conta = numero_conta
        self.agencia_cod = agencia_cod
        self.cpf = cpf
        self._saldo = float(saldo_conta)

    # --- fábricas
    @classmethod
    def criar(cls, tipo, numero_conta, agencia_cod, cpf):
        subclasse = cls._tipos.get(normalizar(tipo))
        if subclasse is None:
            raise ValueError("Tipo de conta inválido.")
        return subclasse(numero_conta, agencia_cod, cpf)

    @classmethod
    def from_dict(cls, d):
        subclasse = cls._tipos[normalizar(d["tipo"])]
        return subclasse(d["numero_conta"], d["agencia_cod"], d["cpf"], d.get("saldo_conta", 0.0))

    # --- estado e permissões
    @property
    def saldo(self):
        return self._saldo

    def permite(self, operacao):
        return operacao in self.OPERACOES_PERMITIDAS

    def validar_operacao(self, operacao):
        if not self.permite(operacao):
            raise ValueError(
                f"A conta {self.numero_conta} ({self.TIPO}) não pode realizar: {operacao}."
            )

    def validar_destino(self, destino):
        if self.numero_conta == destino.numero_conta:
            raise ValueError("A conta de origem e a de destino devem ser diferentes.")

    @staticmethod
    def _saldo_finito(saldo, mensagem):
        if not math.isfinite(saldo):
            raise ValueError(mensagem)
        return saldo

    # --- operações
    def sacar(self, valor):
        self.validar_operacao("sacar")
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente.")
        self._saldo = round(self._saldo - valor, 2)

    def depositar(self, valor):
        self.validar_operacao("depositar")
        self._saldo = self._saldo_finito(
            round(self._saldo + valor, 2), "Valor inválido para o saldo da conta."
        )

    def transferir(self, destino, valor):
        self.validar_operacao("transferir")
        self.validar_destino(destino)
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente.")
        saldo_destino = self._saldo_finito(
            round(destino._saldo + valor, 2), "Valor inválido para o saldo da conta de destino."
        )
        self._saldo = round(self._saldo - valor, 2)
        destino._saldo = saldo_destino

    def to_dict(self):
        return {
            "numero_conta": self.numero_conta,
            "agencia_cod": self.agencia_cod,
            "cpf": self.cpf,
            "saldo_conta": self._saldo,
            "tipo": self.TIPO,
        }


class ContaPoupanca(Conta):
    TIPO = "poupança"
    OPERACOES_PERMITIDAS = frozenset({"sacar", "depositar", "transferir"})
    TAXA_ANUAL = 0.1375  # ligada à Selic

    def aplicar_rendimento(self):
        self._saldo = round(self._saldo * (1 + self.TAXA_ANUAL), 2)


class ContaCorrente(Conta):
    TIPO = "corrente"
    OPERACOES_PERMITIDAS = frozenset({"sacar", "depositar", "transferir"})


class ContaSalario(Conta):
    TIPO = "salário"
    OPERACOES_PERMITIDAS = frozenset({"sacar", "depositar"})  # não transfere
