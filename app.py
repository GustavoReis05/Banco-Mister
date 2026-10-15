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

app.secret_key = "banco-mister"

# Criação do arquivo json
ARQUIVO_DADOS = Path(__file__).parent / "banco_dados.json"


#Função para ler e salvar dados 
def carregar_dados():
    # Função cria um JSON se nao encontrar dentro do diretorio
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


# Inicializaçao do index (pagina inicial)
@app.route("/")
def inicio():
    return render_template("index.html")

# Rota da abertura da pagina de cadastros
@app.route("/cadastro")
def pagina_cadastro():
    return render_template("cadastro.html")

# Rota da aneruta da pagina de listagem
@app.route("/lista")
def pagina_lista():
    dados = carregar_dados()
    return render_template(
        "lista.html",
        clientes=cliente.listar_clientes(dados["clientes"], exibir=False),
        agencias=agencia.listar_agencias(dados["agencias"], exibir=False),
        contas=conta.listar_contas(dados["contas"], exibir=False),
    )


# Abertura da rota para página de busca
@app.route("/busca")
# Lê os dados fornecidos no formulário e conecta com as funçoes de busca dentro de cada arquivo (agencia, conta e cliente)
def pagina_busca():
    tipo = request.args.get("tipo", "cliente")
    termo = request.args.get("termo", "").strip()
    pesquisou = "termo" in request.args
    resultado = None
    mensagem = None

    if tipo not in ("cliente", "agencia", "conta"):
        tipo = "cliente"
        mensagem = "Selecione um tipo de busca válido."
    elif pesquisou:
        if not termo:
            mensagem = "Informe um termo para realizar a busca."
        else:
            dados = carregar_dados()
            if tipo == "cliente":
                # Consulta a existencia do termo de busca dentro da lista de clientes
                resultado = cliente.procurar_cliente(dados["clientes"], termo, exibir=False)
                if resultado is None:
                    mensagem = (
                        "Cliente não encontrado ou nome ambíguo. "
                        "Informe o CPF ou o nome completo."
                    )
            elif tipo == "agencia":
                # Consulta a existencia do termo de busca dentro da lista de agencias
                resultado = agencia.procurar_agencia(dados["agencias"], termo)
                if resultado is None:
                    mensagem = "Agência não encontrada."
            else:
                # Consulta a existencia do termo de busca dentro da lista de contas
                resultado = conta.procurar_conta(dados["contas"], termo)
                if resultado is None:
                    mensagem = "Conta não encontrada."

    return render_template(
        "busca.html", tipo=tipo, termo=termo,
        resultado=resultado, mensagem=mensagem,
    )


#Cadastro de cliente

@app.route("/cadastrar-cliente", methods=["POST"])
def receber_cadastro_cliente():
    # Lê os cadastros existentes.
    dados = carregar_dados()

    try:
        # Lê os dados fornecidos no formulário e conecta com o arquivo cliente
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

    # Acrescenta o cliente no JSON
    dados["clientes"].append(novo_cliente)
    salvar_dados(dados)

    flash("Cliente cadastrado e salvo com sucesso!")
    return redirect(url_for("pagina_cadastro"))


#Cadastro de agencia

@app.route("/cadastrar-agencia", methods=["POST"])
def receber_cadastro_agencia():
    dados = carregar_dados()

    # Lê os dados fornecidos no formulário e conecta com o arquivo agencia
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

#Cadastro de conta 

@app.route("/cadastrar-conta", methods=["POST"])
def cadastrar_conta():
    dados = carregar_dados()

    # Lê os dados fornecidos no formulário e conecta com o arquivo conta
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

# Inicialização do servidor
if __name__ == "__main__":
    app.run(debug=True)