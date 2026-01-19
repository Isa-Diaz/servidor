
from flask import Flask, request, jsonify
from flasgger import Swagger

from ..service.cliente_service import (
    criar_cliente_service,
    atualizar_cliente_service,
    calcular_score,
    operacao_service,
    deletar_cliente_service
)

from ..client.client import listar_clientes, buscar_cliente_por_id

app = Flask(__name__)
swagger = Swagger(app)


@app.route("/clientes", methods=["POST"])
def criar_cliente_controller():
    """
    Criar cliente (microserviço de acesso)
    ---
    tags:
      - Clientes
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            telefone:
              type: string
            correntista:
              type: boolean
            saldo_cc:
              type: number
    responses:
      201:
        description: Cliente criado com sucesso
      400:
        description: Erro de validação
    """
    dados = request.get_json()
    telefone = dados.get("telefone")
    if isinstance(telefone, list):
        telefone = telefone[0]
    dados["telefone"] = telefone

    result = criar_cliente_service(dados)

    if isinstance(result, str):
        return jsonify({"erro": result}), 400

    return jsonify(result), 201


@app.route("/clientes", methods=["GET"])
def listar_clientes_controller():
    """
    Listar clientes (microserviço de acesso)
    ---
    tags:
      - Clientes
    responses:
      200:
        description: Lista de clientes retornada pelo microserviço de armazenamento
    """
    result = listar_clientes()
    return jsonify(result), 200


@app.route("/clientes/<id>", methods=["GET"])
def buscar_cliente_controller(id):
    """
    Buscar cliente por ID
    ---
    tags:
      - Clientes
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Cliente encontrado
      404:
        description: Cliente não encontrado
    """
    result = buscar_cliente_por_id(id)

    if "erro" in result:
        return jsonify(result), 404

    return jsonify(result), 200


@app.route("/clientes/<id>", methods=["PUT"])
def atualizar_cliente_controller(id):
    """
    Atualizar cliente por ID
    ---
    tags:
      - Clientes
    consumes:
      - application/json
    parameters:
      - name: id
        in: path
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            telefone:
              type: string
            correntista:
              type: boolean
    responses:
      200:
        description: Cliente atualizado com sucesso
      400:
        description: Erro de validação
      404:
        description: Cliente não encontrado
    """
    dados = request.get_json()
    result = atualizar_cliente_service(id, dados)

    if isinstance(result, str):
        return jsonify({"erro": result}), 400
    if "erro" in result:
        return jsonify(result), 404

    return jsonify(result), 200


@app.route("/clientes/<id>", methods=["DELETE"])
def deletar_cliente_controller(id):
    """
    Deletar cliente por ID
    ---
    tags:
      - Clientes
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Cliente deletado com sucesso
      400:
        description: Conta com saldo não pode ser deletada
      404:
        description: Cliente não encontrado
    """
    result = deletar_cliente_service(id)

    if "erro" in result:
        return jsonify(result), 400

    return jsonify(result), 200


@app.route("/clientes/<id>/score", methods=["GET"])
def score_controller(id):
    """
    Calcular score de crédito
    ---
    tags:
      - Score
    parameters:
      - name: id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Score calculado com sucesso
      404:
        description: Cliente não encontrado
    """
    result = buscar_cliente_por_id(id)

    if "erro" in result:
        return jsonify(result), 404

    saldo = result.get("saldo_cc", 0)
    score = calcular_score(saldo)

    return jsonify({"id": id, "score": score}), 200


@app.route("/clientes/<id>/operacao", methods=["POST"])
def operacao_controller(id):
    """
    Realizar operação bancária (saque ou depósito)
    ---
    tags:
      - Operações
    consumes:
      - application/json
    parameters:
      - name: id
        in: path
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            tipo:
              type: string
              enum:
                - saque
                - deposito
            valor:
              type: number
    responses:
      200:
        description: Operação realizada com sucesso
      400:
        description: Erro de validação
      404:
        description: Cliente não encontrado
    """
    dados = request.get_json()
    result = operacao_service(id, dados)

    if isinstance(result, str):
        return jsonify({"erro": result}), 400
    if "erro" in result:
        return jsonify(result), 404

    return jsonify(result), 200


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=True, port=5001, host="localhost")  # pragma: no cover

