from unittest.mock import patch
from acesso.controller.cliente_controller import app


def client():
    return app.test_client()


@patch("acesso.controller.cliente_controller.criar_cliente_service", return_value={"id": 1})
def test_criar_cliente_controller(mock_service):
    response = client().post("/clientes", json={"nome": "Ana"})
    assert response.status_code == 201


@patch("acesso.controller.cliente_controller.listar_clientes", return_value=[])
def test_listar_clientes_controller(mock_list):
    response = client().get("/clientes")
    assert response.status_code == 200


@patch("acesso.controller.cliente_controller.buscar_cliente_por_id", return_value={"id": 1})
def test_buscar_cliente_ok(mock_get):
    response = client().get("/clientes/1")
    assert response.status_code == 200


@patch("acesso.controller.cliente_controller.buscar_cliente_por_id", return_value={"erro": "Cliente não encontrado"})
def test_buscar_cliente_erro(mock_get):
    response = client().get("/clientes/1")
    assert response.status_code == 404


@patch("acesso.controller.cliente_controller.atualizar_cliente_service", return_value={"ok": True})
def test_atualizar_cliente(mock_update):
    response = client().put("/clientes/1", json={})
    assert response.status_code == 200


@patch("acesso.controller.cliente_controller.atualizar_cliente_service", return_value="Erro")
def test_atualizar_cliente_erro(mock_update):
    response = client().put("/clientes/1", json={})
    assert response.status_code == 400


@patch("acesso.controller.cliente_controller.atualizar_cliente_service", return_value={"erro": "não encontrado"})
def test_atualizar_cliente_notfound(mock_update):
    response = client().put("/clientes/1", json={})
    assert response.status_code == 404


@patch("acesso.controller.cliente_controller.deletar_cliente_service", return_value={"sucesso": True})
def test_deletar_cliente_ok(mock_delete):
    response = client().delete("/clientes/1")
    assert response.status_code == 200


@patch("acesso.controller.cliente_controller.deletar_cliente_service", return_value={"erro": "x"})
def test_deletar_cliente_erro(mock_delete):
    response = client().delete("/clientes/1")
    assert response.status_code == 400


@patch("acesso.controller.cliente_controller.buscar_cliente_por_id", return_value={"saldo_cc": 100})
@patch("acesso.controller.cliente_controller.calcular_score", return_value=10)
def test_score_controller(mock_score, mock_get):
    response = client().get("/clientes/1/score")
    assert response.status_code == 200


@patch("acesso.controller.cliente_controller.buscar_cliente_por_id", return_value={"erro": "x"})
def test_score_controller_erro(mock_get):
    response = client().get("/clientes/1/score")
    assert response.status_code == 404


@patch("acesso.controller.cliente_controller.operacao_service", return_value={"ok": True})
def test_operacao_controller(mock_op):
    response = client().post("/clientes/1/operacao", json={})
    assert response.status_code == 200


@patch("acesso.controller.cliente_controller.operacao_service", return_value="erro")
def test_operacao_controller_erro_400(mock_op):
    response = client().post("/clientes/1/operacao", json={})
    assert response.status_code == 400


@patch("acesso.controller.cliente_controller.operacao_service", return_value={"erro": "x"})
def test_operacao_controller_erro_404(mock_op):
    response = client().post("/clientes/1/operacao", json={})
    assert response.status_code == 404
