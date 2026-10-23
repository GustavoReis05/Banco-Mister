import json
from functools import partial
from pathlib import Path

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

import agencia
import cliente
import conta

app = Flask(__name__)

app.secret_key = "banco-mister"

# Criação do arquivo json
ARQUIVO_DADOS = Path(__file__).parent / "banco_dados.json"

COLECOES = ("clientes", "agencias", "contas")


# ---------- Leitura e gravação dos dados ----------

def carregar_dados():
    # Se o arquivo não existir, devolve as três coleções vazias
    if not ARQUIVO_DADOS.exists():
        return {colecao: [] for colecao in COLECOES}

    with ARQUIVO_DADOS.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_dados(dados):
    with ARQUIVO_DADOS.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


# ---------- Função de ordem superior para os cadastros ----------

def tratar_cadastro(colecao, cadastrar, campos_form, mensagem_sucesso, **listas):
    """Executa o fluxo comum de cadastro.

    colecao:      chave em `dados` onde o novo registro será salvo
    cadastrar:    função de cadastro (cliente, agência ou conta)
    campos_form:  {parâmetro_da_função: nome_do_campo_no_formulário}
    listas:       {parâmetro_da_função: chave em `dados`} para as listas que a função consulta
    """
    dados = carregar_dados()

    try:
        novo = cadastrar(
            **{param: dados[chave] for param, chave in listas.items()},
            **{param: request.form.get(campo, "") for param, campo in campos_form.items()},
        )
    except ValueError as erro:
        flash(str(erro))
        return redirect(url_for("pagina_cadastro"))

    dados[colecao].append(novo)
    salvar_dados(dados)

    flash(mensagem_sucesso)
    return redirect(url_for("pagina_cadastro"))


# ---------- Tabelas usadas por listagem, busca e operações ----------

# Função de listagem de cada coleção
LISTADORES = {
    "clientes": cliente.listar_clientes,
    "agencias": agencia.listar_agencias,
    "contas": conta.listar_contas,
}

# tipo de busca -> (coleção, função de busca, mensagem quando não encontra)
BUSCAS = {
    "cliente": (
        "clientes",
        partial(cliente.procurar_cliente, exibir=False),
        "Cliente não encontrado ou nome ambíguo. Informe o CPF ou o nome completo.",
    ),
    "agencia": ("agencias", agencia.procurar_agencia, "Agência não encontrada."),
    "conta": ("contas", conta.procurar_conta, "Conta não encontrada."),
}

# operação -> função que recebe (lista_contas, formulário)
OPERACOES = {
    "sacar": lambda contas, form: conta.sacar(
        contas, form.get("numero_conta", ""), form.get("valor", "")
    ),
    "depositar": lambda contas, form: conta.depositar(
        contas, form.get("numero_conta", ""), form.get("valor", "")
    ),
    "transferir": lambda contas, form: conta.transferir(
        contas,
        form.get("numero_conta", ""),
        form.get("numero_destino", ""),
        form.get("valor", ""),
    ),
}


"""Dashboard e inicialização do index.html"""
@app.route("/")
def inicio():
    dados = carregar_dados()

    listagens = {
        "numero_clientes": (
            cliente.listar_clientes,
            dados["clientes"],
        ),
        "numero_agencias": (
            agencia.listar_agencias,
            dados["agencias"],
        ),
        "numero_contas": (
            conta.listar_contas,
            dados["contas"],
        ),
    }

    quantidades = {nome: len(listar(registros)) for nome, (listar, registros) in listagens.items()}

    indicadores_saldos = conta.calcular_indicadores_saldos(dados["contas"])

    return render_template("index.html", **quantidades, **indicadores_saldos,montante_total=indicadores_saldos["saldo_total"])

# Página de cadastros
@app.route("/cadastro")
def pagina_cadastro():
    return render_template("cadastro.html")


# Cadastro de cliente
@app.route("/cadastrar-cliente", methods=["POST"])
def receber_cadastro_cliente():
    return tratar_cadastro(
        "clientes",
        cliente.cadastrar_cliente,
        {campo: campo for campo in ("cpf", "nome", "data_nascimento", "numero_telefone")},
        "Cliente cadastrado e salvo com sucesso!",
        lista_clientes="clientes",
    )


# Cadastro de agência
@app.route("/cadastrar-agencia", methods=["POST"])
def receber_cadastro_agencia():
    return tratar_cadastro(
        "agencias",
        agencia.cadastrar_agencia,
        {
            "codigo": "codigo_agencia",
            "nome": "nome_agencia",
            "cidade_estado": "cidade_estado",
        },
        "Agência cadastrada e salva com sucesso!",
        lista_agencias="agencias",
    )


# Cadastro de conta
@app.route("/cadastrar-conta", methods=["POST"])
def cadastrar_conta():
    return tratar_cadastro(
        "contas",
        conta.cadastrar_conta,
        {campo: campo for campo in ("termo_busca", "agencia_cod", "numero_conta", "tipo")},
        "Conta cadastrada e salva com sucesso!",
        lista_clientes="clientes",
        lista_agencias="agencias",
        lista_contas="contas",
    )


# Página de listagem
@app.route("/lista")
def pagina_lista():
    dados = carregar_dados()

    return render_template(
        "lista.html",
        **{colecao: listar(dados[colecao]) for colecao, listar in LISTADORES.items()},
    )


# Página de busca
@app.route("/busca")
def pagina_busca():
    tipo = request.args.get("tipo", "cliente")
    termo = request.args.get("termo", "").strip()
    pesquisou = "termo" in request.args
    resultado = None
    mensagem = None

    if tipo not in BUSCAS:
        tipo = "cliente"
        mensagem = "Selecione um tipo de busca válido."
    elif pesquisou:
        if not termo:
            mensagem = "Informe um termo para realizar a busca."
        else:
            colecao, buscar, mensagem_nao_encontrado = BUSCAS[tipo]
            resultado = buscar(carregar_dados()[colecao], termo)
            if resultado is None:
                mensagem = mensagem_nao_encontrado

    return render_template(
        "busca.html", tipo=tipo, termo=termo,
        resultado=resultado, mensagem=mensagem,
    )

"""Operações do banco"""
@app.route("/operacoes", methods=["GET", "POST"])
def pagina_operacoes():
    if request.method == "POST":
        dados = carregar_dados()
        executar = OPERACOES.get(request.form.get("operacao", ""))

        try:
            if executar is None:
                raise ValueError("Selecione uma operação válida.")
            mensagem = executar(dados["contas"], request.form)
        except ValueError as erro:
            flash(str(erro))
        else:
            salvar_dados(dados)
            flash(mensagem)
        return redirect(url_for("pagina_operacoes"))
    return render_template("operacoes.html")


@app.route("/min_max_saldo")
def pagina_extremos_saldos():
    dados = carregar_dados()

    extremos = conta.encontrar_menor_maior_saldo(
        dados["contas"]
    )

    return render_template(
        "min_max_saldo.html",
        possui_contas=bool(dados["contas"]),
        **extremos,
    )


# Inicialização do servidor
if __name__ == "__main__":
    app.run(debug=True)
