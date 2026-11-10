from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

from banco import Banco, RepositorioJSON


class BancoMisterApp:
    """Encapsula o Flask, as rotas e o acesso ao Banco."""

    BUSCAS = {
        "cliente": (
            lambda banco, termo: banco.procurar_cliente(termo),
            "Cliente não encontrado ou nome ambíguo. Informe o CPF ou o nome completo.",
        ),
        "agencia": (lambda banco, termo: banco.procurar_agencia(termo), "Agência não encontrada."),
        "conta": (lambda banco, termo: banco.procurar_conta(termo), "Conta não encontrada."),
    }

    OPERACOES = {
        "sacar": lambda banco, f: banco.sacar(f.get("numero_conta", ""), f.get("valor", "")),
        "depositar": lambda banco, f: banco.depositar(f.get("numero_conta", ""), f.get("valor", "")),
        "transferir": lambda banco, f: banco.transferir(
            f.get("numero_conta", ""), f.get("numero_destino", ""), f.get("valor", "")
        ),
    }

    def __init__(self, arquivo_dados=None):
        self.flask = Flask(__name__)
        self.flask.secret_key = "banco-mister"
        self.repositorio = RepositorioJSON(arquivo_dados or Path(__file__).parent / "banco_dados.json")
        self._registrar_rotas()

    # ---------------------------------------------------------- utilitários
    def _banco(self):
        return Banco(self.repositorio)

    def _cadastrar(self, acao, mensagem_sucesso, **campos):
        """Fluxo comum dos três cadastros."""
        banco = self._banco()
        try:
            acao(banco)(**{p: request.form.get(c, "") for p, c in campos.items()})
        except ValueError as erro:
            flash(str(erro))
        else:
            banco.salvar()
            flash(mensagem_sucesso)
        return redirect(url_for("pagina_cadastro"))

    def _registrar_rotas(self):
        rotas = [
            ("/", "inicio", self.inicio, ["GET"]),
            ("/cadastro", "pagina_cadastro", self.pagina_cadastro, ["GET"]),
            ("/cadastrar-cliente", "receber_cadastro_cliente", self.cadastrar_cliente, ["POST"]),
            ("/cadastrar-agencia", "receber_cadastro_agencia", self.cadastrar_agencia, ["POST"]),
            ("/cadastrar-conta", "cadastrar_conta", self.cadastrar_conta, ["POST"]),
            ("/lista", "pagina_lista", self.pagina_lista, ["GET"]),
            ("/busca", "pagina_busca", self.pagina_busca, ["GET"]),
            ("/operacoes", "pagina_operacoes", self.pagina_operacoes, ["GET", "POST"]),
            ("/min_max_saldo", "pagina_extremos_saldos", self.pagina_extremos_saldos, ["GET"]),
        ]
        for caminho, endpoint, view, metodos in rotas:
            self.flask.add_url_rule(caminho, endpoint, view, methods=metodos)

    # --------------------------------------------------------------- rotas
    def inicio(self):
        banco = self._banco()
        indicadores = banco.indicadores_saldos()
        return render_template(
            "index.html",
            numero_clientes=len(banco.clientes),
            numero_agencias=len(banco.agencias),
            numero_contas=len(banco.contas),
            montante_total=indicadores["saldo_total"],
            **indicadores,
        )

    def pagina_cadastro(self):
        return render_template("cadastro.html")

    def cadastrar_cliente(self):
        return self._cadastrar(
            lambda b: b.cadastrar_cliente,
            "Cliente cadastrado e salvo com sucesso!",
            cpf="cpf", nome="nome",
            data_nascimento="data_nascimento", numero_telefone="numero_telefone",
        )

    def cadastrar_agencia(self):
        return self._cadastrar(
            lambda b: b.cadastrar_agencia,
            "Agência cadastrada e salva com sucesso!",
            codigo="codigo_agencia", nome="nome_agencia", cidade_estado="cidade_estado",
        )

    def cadastrar_conta(self):
        return self._cadastrar(
            lambda b: b.cadastrar_conta,
            "Conta cadastrada e salva com sucesso!",
            termo_busca="termo_busca", agencia_cod="agencia_cod",
            numero_conta="numero_conta", tipo="tipo",
        )

    def pagina_lista(self):
        banco = self._banco()
        return render_template(
            "lista.html",
            clientes=[c.to_dict() for c in banco.clientes],
            agencias=[a.to_dict() for a in banco.agencias],
            contas=[c.to_dict() for c in banco.contas],
        )

    def pagina_busca(self):
        tipo = request.args.get("tipo", "cliente")
        termo = request.args.get("termo", "").strip()
        resultado, mensagem = None, None

        if tipo not in self.BUSCAS:
            tipo = "cliente"
            mensagem = "Selecione um tipo de busca válido."
        elif "termo" in request.args:
            if not termo:
                mensagem = "Informe um termo para realizar a busca."
            else:
                buscar, mensagem_nao_encontrado = self.BUSCAS[tipo]
                encontrado = buscar(self._banco(), termo)
                if encontrado is None:
                    mensagem = mensagem_nao_encontrado
                else:
                    resultado = encontrado.to_dict()

        return render_template("busca.html", tipo=tipo, termo=termo, resultado=resultado, mensagem=mensagem)

    def pagina_operacoes(self):
        if request.method == "POST":
            banco = self._banco()
            executar = self.OPERACOES.get(request.form.get("operacao", ""))
            try:
                if executar is None:
                    raise ValueError("Selecione uma operação válida.")
                mensagem = executar(banco, request.form)
            except ValueError as erro:
                flash(str(erro))
            else:
                banco.salvar()
                flash(mensagem)
            return redirect(url_for("pagina_operacoes"))
        return render_template("operacoes.html")

    def pagina_extremos_saldos(self):
        banco = self._banco()
        return render_template(
            "min_max_saldo.html",
            possui_contas=bool(banco.contas),
            **banco.extremos_saldos(),
        )

    def executar(self, **kwargs):
        self.flask.run(**kwargs)


app = BancoMisterApp().flask  # exposto para `flask run` / gunicorn

if __name__ == "__main__":
    BancoMisterApp().executar(debug=True)
