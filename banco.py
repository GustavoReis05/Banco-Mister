Claude




































Banco · PY
"""Camada de serviço: guarda as coleções, aplica regras e persiste em JSON."""
import json
from pathlib import Path
 
from modelos import Agencia, Cliente, Conta, apenas_digitos, validar_valor_operacao
 
 
class RepositorioJSON:
    """Responsável apenas por ler e gravar o arquivo."""
 
    COLECOES = ("clientes", "agencias", "contas")
 
    def __init__(self, caminho):
        self.caminho = Path(caminho)
 
    def carregar(self):
        if not self.caminho.exists():
            return {colecao: [] for colecao in self.COLECOES}
        with self.caminho.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
 
    def salvar(self, dados):
        with self.caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
 
 
class Banco:
    def __init__(self, repositorio):
        self._repositorio = repositorio
        dados = repositorio.carregar()
        self.clientes = [Cliente.from_dict(d) for d in dados.get("clientes", [])]
        self.agencias = [Agencia.from_dict(d) for d in dados.get("agencias", [])]
        self.contas = [Conta.from_dict(d) for d in dados.get("contas", [])]
 
    def salvar(self):
        self._repositorio.salvar({
            "clientes": [c.to_dict() for c in self.clientes],
            "agencias": [a.to_dict() for a in self.agencias],
            "contas": [c.to_dict() for c in self.contas],
        })
 
    # ------------------------------------------------------------ buscas
    def procurar_cliente(self, termo):
        """Por CPF ou nome. Retorna None se não achar ou se for ambíguo."""
        termo = termo.strip()
        if not termo:
            return None
        exato = next((c for c in self.clientes if c.corresponde_exato(termo)), None)
        if exato:
            return exato
        candidatos = [c for c in self.clientes if c.corresponde_parcial(termo)]
        return candidatos[0] if len(candidatos) == 1 else None
 
    def procurar_agencia(self, codigo):
        return next((a for a in self.agencias if a.codigo == codigo.strip()), None)
 
    def procurar_conta(self, numero):
        numero = str(numero).strip()
        return next((c for c in self.contas if c.numero_conta == numero), None)
 
    def _conta_para(self, numero, operacao):
        """Conta existente cujo tipo permite a operação."""
        conta = self.procurar_conta(numero)
        if conta is None:
            raise ValueError("Conta não encontrada!")
        conta.validar_operacao(operacao)
        return conta
 
    # ----------------------------------------------------------- cadastros
    def cadastrar_cliente(self, cpf, nome, data_nascimento, numero_telefone):
        novo = Cliente.criar(cpf, nome, data_nascimento, numero_telefone)
        if any(apenas_digitos(c.cpf) == apenas_digitos(novo.cpf) for c in self.clientes):
            raise ValueError("Já existe um cliente com esse CPF.")
        self.clientes.append(novo)
        return novo
 
    def cadastrar_agencia(self, codigo, nome, cidade_estado):
        nova = Agencia.criar(codigo, nome, cidade_estado)
        if self.procurar_agencia(nova.codigo):
            raise ValueError("Já existe uma agência com esse código.")
        self.agencias.append(nova)
        return nova
 
    def cadastrar_conta(self, termo_busca, agencia_cod, numero_conta, tipo):
        termo_busca, agencia_cod, numero_conta, tipo = (
            t.strip() for t in (termo_busca, agencia_cod, numero_conta, tipo)
        )
        if not all((termo_busca, agencia_cod, numero_conta, tipo)):
            raise ValueError("Preencha todos os campos da conta.")
 
        cliente = self.procurar_cliente(termo_busca)
        if cliente is None:
            raise ValueError("Cliente não encontrado ou nome ambíguo. Informe o CPF ou o nome completo.")
        if self.procurar_agencia(agencia_cod) is None:
            raise ValueError("Agência não encontrada.")
        if self.procurar_conta(numero_conta):
            raise ValueError("Já existe uma conta com esse número.")
 
        nova = Conta.criar(tipo, numero_conta, agencia_cod, cliente.cpf)
        self.contas.append(nova)
        return nova
 
    # ----------------------------------------------------------- operações
    def sacar(self, numero_conta, valor):
        conta = self._conta_para(numero_conta, "sacar")
        valor = validar_valor_operacao(valor)
        conta.sacar(valor)
        return f"Saque de R$ {valor:.2f} realizado com sucesso!"
 
    def depositar(self, numero_conta, valor):
        conta = self._conta_para(numero_conta, "depositar")
        valor = validar_valor_operacao(valor)
        conta.depositar(valor)
        return f"Depósito de R$ {valor:.2f} realizado com sucesso!"
 
    def transferir(self, numero_origem, numero_destino, valor):
        origem = self._conta_para(numero_origem, "transferir")
        destino = self.procurar_conta(numero_destino)
        if destino is None:
            raise ValueError("Conta de destino não encontrada!")
        origem.validar_destino(destino)
        valor = validar_valor_operacao(valor)
        origem.transferir(destino, valor)
        return "Transferência realizada com sucesso!"
 
    # ---------------------------------------------------------- indicadores
    def _saldos(self):
        return [c.saldo for c in self.contas]
 
    def indicadores_saldos(self):
        """Valores do dashboard: saldo_total, maior_saldo e saldo_medio."""
        saldos = self._saldos()
        total = sum(saldos, 0.0)
        return {
            "saldo_total": total,
            "maior_saldo": max(saldos, default=0.0),
            "saldo_medio": total / len(saldos) if saldos else 0.0,
        }
 
    def extremos_saldos(self):
        """Menor e maior saldo (números, não contas), como no conta.py."""
        saldos = self._saldos()
        return {
            "menor_saldo": min(saldos, default=0.0),
            "maior_saldo": max(saldos, default=0.0),
        }
 
