from unittest.mock import patch
from micro_servico.controller.storage_controller import app


def client():
    return app.test_client()


def test_status():
    response = client().get("/status")
    assert response.status_code == 200
    assert response.json == {"mensagem": "Microserviço de Armazenamento está funcionando."}


@patch("micro_servico.controller.storage_controller.insert_cliente", return_value=1)
def test_criar_cliente(mock_insert):
    response = client().post("/clientes", json={
        "nome": "Ana",
        "telefone": 123,
        "correntista": True,
        "score_credito": 10,
        "saldo_cc": 100
    })
    assert response.status_code == 201
    assert response.json["id"] == 1


@patch("micro_servico.controller.storage_controller.listar_clientes", return_value=[
    (1, "Ana", 123, True, 10.0, 100.0)
])
def test_listar(mock_list):
    response = client().get("/clientes")
    assert response.status_code == 200
    assert response.json[0]["id"] == 1


@patch("micro_servico.controller.storage_controller.buscar_cliente_por_id",
       return_value=(1, "Ana", 123, True, 10.0, 100.0))
def test_buscar_cliente_ok(mock_get):
    response = client().get("/clientes/1")
    assert response.status_code == 200
    assert response.json["nome"] == "Ana"


@patch("micro_servico.controller.storage_controller.buscar_cliente_por_id",
       return_value=None)
def test_buscar_cliente_not_found(mock_get):
    response = client().get("/clientes/1")
    assert response.status_code == 404
    assert response.json == {"erro": "Cliente não encontrado"}


@patch("micro_servico.controller.storage_controller.atualizar_cliente")
@patch("micro_servico.controller.storage_controller.buscar_cliente_por_id",
       return_value=(1, "Ana", 123, True, 10.0, 100.0))
def test_atualizar_cliente_ok(mock_get, mock_update):
    response = client().put("/clientes/1", json={
        "nome": "Ana",
        "telefone": 123,
        "correntista": True,
        "score_credito": 10,
        "saldo_cc": 200
    })
    assert response.status_code == 200
    assert response.json["id"] == 1


@patch("micro_servico.controller.storage_controller.buscar_cliente_por_id",
       return_value=None)
def test_atualizar_cliente_not_found(mock_get):
    response = client().put("/clientes/1", json={
        "nome": "Ana"
    })
    
    assert response.status_code == 404
    assert response.json == {"erro": "Cliente não encontrado"}


@patch("micro_servico.controller.storage_controller.delete_cliente")
@patch("micro_servico.controller.storage_controller.buscar_cliente_por_id",
       return_value=(1, "Ana", 123, True, 10.0, 100.0))
def test_excluir_cliente_ok(mock_get, mock_delete):
    response = client().delete("/clientes/1")
    assert response.status_code == 200
    assert response.json == {"sucesso": "Cliente deletado"}


@patch("micro_servico.controller.storage_controller.buscar_cliente_por_id",
       return_value=None)
def test_excluir_cliente_not_found(mock_get):
    response = client().delete("/clientes/1")
    assert response.status_code == 404
    assert response.json == {"erro": "Cliente não encontrado"}
