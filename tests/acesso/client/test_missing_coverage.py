from unittest.mock import patch, MagicMock
import acesso.client.client as client
from acesso.controller.cliente_controller import app
from micro_servico.controller.storage_controller import app as storage_app


def make_mock_response(text):
    mock = MagicMock()
    mock.json.side_effect = ValueError("invalid json")
    mock.text = text
    return mock

@patch("requests.get", return_value=make_mock_response("X"))
def test_listar_clientes_resposta_invalida(mock):
    out = client.listar_clientes()
    assert out["erro"] == "Resposta inválida do microserviço"

@patch("requests.get", return_value=make_mock_response("Y"))
def test_buscar_cliente_por_id_resposta_invalida(mock):
    out = client.buscar_cliente_por_id(1)
    assert out["erro"] == "Resposta inválida do microserviço"

@patch("requests.post", return_value=make_mock_response("Z"))
def test_criar_cliente_resposta_invalida(mock):
    out = client.criar_cliente({})
    assert out["erro"] == "Resposta inválida do microserviço"

@patch("requests.put", return_value=make_mock_response("W"))
def test_atualizar_cliente_resposta_invalida(mock):
    out = client.atualizar_cliente(1, {})
    assert "erro" in out

@patch("requests.delete", return_value=make_mock_response("Q"))
def test_deletar_cliente_resposta_invalida(mock):
    out = client.deletar_cliente(1)
    assert "erro" in out

def test_criar_cliente_controller_telefone_lista():
    client_app = app.test_client()
    with patch("acesso.controller.cliente_controller.criar_cliente_service", return_value={"ok": True}):
        resp = client_app.post("/clientes", json={
            "nome": "Ana",
            "telefone": ["11999999999"],
            "correntista": True,
            "saldo_cc": 0
        })
        assert resp.status_code == 201

def test_import_main_guard():
    import acesso.controller.cliente_controller
    assert True  

def test_storage_criar_cliente_telefone_lista():
    client_s = storage_app.test_client()
    with patch("micro_servico.controller.storage_controller.insert_cliente", return_value=99):
        resp = client_s.post("/clientes", json={
            "nome": "Ana",
            "telefone": ["99999999999"],
            "correntista": True,
            "score_credito": 10,
            "saldo_cc": 100
        })
        assert resp.status_code == 201
        assert resp.json["id"] == 99
