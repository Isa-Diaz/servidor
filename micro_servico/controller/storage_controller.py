from flask import Flask, request, jsonify
from flasgger import Swagger
from micro_servico.repository.storage_repository import (
    create_table,
    insert_cliente,
    listar_clientes,
    buscar_cliente_por_id,
    atualizar_cliente,
    delete_cliente
)

app = Flask(__name__)
swagger = Swagger(app)
create_table()

@app.route("/status", methods=["GET"])
def status():
    """
    Verificar status do microserviço
    ---
    tags:
      - Status
    responses:
      200:
        description: Serviço funcionando
    """
    return jsonify({"mensagem": "Microserviço de Armazenamento está funcionando."})

@app.route("/clientes", methods=["POST"])
def criar_cliente():
    """
    Criar cliente no armazenamento
    ---
    tags:
      - Clientes
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              nome:
                type: string
              telefone:
                type: string
              correntista:
                type: boolean
              score_credito:
                type: number
              saldo_cc:
                type: number
    responses:
      201:
        description: Cliente criado com sucesso
    """
    dados = request.get_json()
    telefone = dados.get("telefone")
    if isinstance(telefone, list):
        telefone = telefone[0]
    dados["telefone"] = telefone

    cliente_id = insert_cliente(
        dados.get("nome"),
        dados.get("telefone"),
        dados.get("correntista"),
        dados.get("score_credito"),
        dados.get("saldo_cc")
    )

    dados["id"] = cliente_id
    return jsonify(dados), 201


@app.route("/clientes", methods=["GET"])
def listar():
    """
    Listar todos os clientes
    ---
    tags:
      - Clientes
    responses:
      200:
        description: Lista de clientes cadastrados
    """
    linhas = listar_clientes()
    lista = []

    for linha in linhas:
        lista.append({
            "id": linha[0],
            "nome": linha[1],
            "telefone": linha[2],
            "correntista": linha[3],
            "score_credito": linha[4],
            "saldo_cc": linha[5],
        })
    return jsonify(lista)

@app.route("/clientes/<id>", methods=["GET"])
def buscar(id):
    """
    Buscar cliente por ID
    ---
    tags:
      - Clientes
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Cliente encontrado
      404:
        description: Cliente não encontrado
    """
    linha = buscar_cliente_por_id(int(id))

    if not linha:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    cliente = {
        "id": linha[0],
        "nome": linha[1],
        "telefone": linha[2],
        "correntista": linha[3],
        "score_credito": linha[4],
        "saldo_cc": linha[5],
    }

    return jsonify(cliente)

@app.route("/clientes/<id>", methods=["PUT"])
def atualizar(id):
    """
    Atualizar cliente por ID
    ---
    tags:
      - Clientes
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              nome:
                type: string
              telefone:
                type: string
              correntista:
                type: boolean
              score_credito:
                type: number
              saldo_cc:
                type: number
    responses:
      200:
        description: Cliente atualizado
      404:
        description: Cliente não encontrado
    """
    dados = request.get_json()

    linha = buscar_cliente_por_id(int(id))
    if not linha:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    atualizar_cliente(
        int(id),
        dados.get("nome"),
        dados.get("telefone"),
        dados.get("correntista"),
        dados.get("score_credito"),
        dados.get("saldo_cc")
    )

    dados["id"] = int(id)
    return jsonify(dados), 200

@app.route("/clientes/<id>", methods=["DELETE"])
def excluir(id):
    """
    Excluir cliente por ID
    ---
    tags:
      - Clientes
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Cliente deletado
      404:
        description: Cliente não encontrado
    """
    linha = buscar_cliente_por_id(int(id))

    if not linha:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    delete_cliente(int(id))

    return jsonify({"sucesso": "Cliente deletado"}), 200


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=True)  # pragma: no cover
