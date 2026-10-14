import json
from datetime import date
from pathlib import Path

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

import cliente
import agencia 
import conta

app = Flask(__name__)

# Necessária para mostrar mensagens com flash().
# Esta chave é apenas para desenvolvimento local.
app.secret_key = "banco-mister-desenvolvimento"

# O arquivo será criado na mesma pasta deste web.py.
ARQUIVO_DADOS = Path(__file__).parent / "banco_dados.json"


# --------------------------------------------------
# FUNÇÕES PARA LER E SALVAR OS DADOS
# --------------------------------------------------

def carregar_dados():
    if not ARQUIVO_DADOS.exists():
        return {
            "clientes": [],
            "agencias": [],
            "contas": [],
        }

    with ARQUIVO_DADOS.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_dados(dados):
    with ARQUIVO_DADOS.open("w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False,
        )


# --------------------------------------------------
# PÁGINAS
# --------------------------------------------------

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/cadastro")
def pagina_cadastro():
    return render_template("cadastro.html")


# --------------------------------------------------
# CADASTRO DE CLIENTE
# --------------------------------------------------

@app.route("/cadastrar-cliente", methods=["POST"])
def receber_cadastro_cliente():
    # Lê os cadastros existentes.
    dados = carregar_dados()

    try:
        # Envia os campos do formulário para cliente.py.
        novo_cliente = cliente.cadastrar_cliente(
            lista_clientes=dados["clientes"],
            cpf=request.form.get("cpf", ""),
            nome=request.form.get("nome", ""),
            data_nascimento=request.form.get("data_nascimento", ""),
            numero_telefone=request.form.get("numero_telefone", ""),
        )

    except ValueError as erro:
        flash(str(erro))
        return redirect(url_for("pagina_cadastro"))

    # Acrescenta o cliente e salva no JSON.
    dados["clientes"].append(novo_cliente)
    salvar_dados(dados)

    flash("Cliente cadastrado e salvo com sucesso!")
    return redirect(url_for("pagina_cadastro"))

# --------------------------------------------------
# CADASTRO DE AGÊNCIA
# --------------------------------------------------

@app.route("/cadastrar-agencia", methods=["POST"])
def receber_cadastro_agencia():
    dados = carregar_dados()

    try:
        nova_agencia = agencia.cadastrar_agencia(
            lista_agencias=dados["agencias"],
            codigo=request.form.get("codigo_agencia", ""),
            nome=request.form.get("nome_agencia", ""),
            cidade_estado=request.form.get("cidade_estado", ""),
        )
    except ValueError as erro:
        flash(str(erro))
        return redirect(url_for("pagina_cadastro"))

    dados["agencias"].append(nova_agencia)
    salvar_dados(dados)

    flash("Agência cadastrada e salva com sucesso!")
    return redirect(url_for("pagina_cadastro"))

# --------------------------------------------------
# CADASTRO DE CONTA
# --------------------------------------------------

@app.route("/cadastrar-conta", methods=["POST"])
def cadastrar_conta():
    dados = carregar_dados()

    try:
        nova_conta = conta.cadastrar_conta(
            lista_clientes=dados["clientes"],
            lista_agencias=dados["agencias"],
            lista_contas=dados["contas"],
            termo_busca=request.form.get("termo_busca", ""),
            agencia_cod=request.form.get("agencia_cod", ""),
            numero_conta=request.form.get("numero_conta", ""),
            tipo=request.form.get("tipo", ""),
        )
    except ValueError as erro:
        flash(str(erro))
        return redirect(url_for("pagina_cadastro"))

    dados["contas"].append(nova_conta)
    salvar_dados(dados)

    flash("Conta cadastrada e salva com sucesso!")
    return redirect(url_for("pagina_cadastro"))
# --------------------------------------------------
# INICIAR O SERVIDOR
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)