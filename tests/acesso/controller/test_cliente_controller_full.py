import pytest
from flask import json
from acesso.controller.cliente_controller import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# --- POST /clientes ---
def test_criar_cliente_controller(client):
    dados = {"nome": "Ana", "telefone": "11999999999", "correntista": True, "saldo_cc": 100}
    resposta_mock = {"id": 1, "nome": "Ana", "telefone": 11999999999, "correntista": True, "saldo_cc": 100, "score_credito": 10}

    with patch("acesso.controller.cliente_controller.criar_cliente_service", return_value=resposta_mock):
        resp = client.post("/clientes", json=dados)
        assert resp.status_code == 201
        assert resp.get_json() == resposta_mock

# --- GET /clientes ---
def test_listar_clientes_controller(client):
    resposta_mock = [{"id":1,"nome":"Ana"}]
    with patch("acesso.controller.cliente_controller.listar_clientes", return_value=resposta_mock):
        resp = client.get("/clientes")
        assert resp.status_code == 200
        assert resp.get_json() == resposta_mock

# --- GET /clientes/<id> ---
def test_buscar_cliente_controller_ok(client):
    resposta_mock = {"id": 1, "nome": "Ana"}
    with patch("acesso.controller.cliente_controller.buscar_cliente_por_id", return_value=resposta_mock):
        resp = client.get("/clientes/1")
        assert resp.status_code == 200
        assert resp.get_json() == resposta_mock

def test_buscar_cliente_controller_erro(client):
    with patch("acesso.controller.cliente_controller.buscar_cliente_por_id", return_value={"erro": "Não encontrado"}):
        resp = client.get("/clientes/999")
        assert resp.status_code == 404
        assert resp.get_json() == {"erro": "Não encontrado"}

# --- PUT /clientes/<id> ---
def test_atualizar_cliente_controller(client):
    dados = {"nome": "Maria"}
    resposta_mock = {"id": 1, "nome": "Maria"}

    with patch("acesso.controller.cliente_controller.atualizar_cliente_service", return_value=resposta_mock):
        resp = client.put("/clientes/1", json=dados)
        assert resp.status_code == 200
        assert resp.get_json() == resposta_mock

def test_atualizar_cliente_controller_erro(client):
    dados = {"telefone": "12AB"}
    with patch("acesso.controller.cliente_controller.atualizar_cliente_service", return_value={"erro": "Inválido"}):
        resp = client.put("/clientes/1", json=dados)
        assert resp.status_code == 404
        assert resp.get_json() == {"erro": "Inválido"}

# --- DELETE /clientes/<id> ---
def test_deletar_cliente_controller(client):
    with patch("acesso.controller.cliente_controller.deletar_cliente_service", return_value={"ok": True}):
        resp = client.delete("/clientes/1")
        assert resp.status_code == 200
        assert resp.get_json() == {"ok": True}

def test_deletar_cliente_controller_erro(client):
    with patch("acesso.controller.cliente_controller.deletar_cliente_service", return_value={"erro": "Saldo não zero"}):
        resp = client.delete("/clientes/1")
        assert resp.status_code == 400
        assert resp.get_json() == {"erro": "Saldo não zero"}

# --- GET /clientes/<id>/score ---
def test_score_controller(client):
    with patch("acesso.controller.cliente_controller.buscar_cliente_por_id", return_value={"id":1,"saldo_cc":100}):
        with patch("acesso.controller.cliente_controller.calcular_score", return_value=10):
            resp = client.get("/clientes/1/score")
            assert resp.status_code == 200
            assert resp.get_json() == {"id": "1", "score": 10}


def test_score_controller_erro(client):
    with patch("acesso.controller.cliente_controller.buscar_cliente_por_id", return_value={"erro": "Não encontrado"}):
        resp = client.get("/clientes/1/score")
        assert resp.status_code == 404
        assert resp.get_json() == {"erro": "Não encontrado"}

# --- POST /clientes/<id>/operacao ---
def test_operacao_controller_deposito(client):
    dados = {"tipo": "deposito", "valor": 100}
    with patch("acesso.controller.cliente_controller.operacao_service", return_value={"saldo_cc":200}):
        resp = client.post("/clientes/1/operacao", json=dados)
        assert resp.status_code == 200
        assert resp.get_json() == {"saldo_cc":200}

def test_operacao_controller_erro(client):
    dados = {"tipo": "deposito", "valor": 100}
    with patch("acesso.controller.cliente_controller.operacao_service", return_value="Erro"):
        resp = client.post("/clientes/1/operacao", json=dados)
        assert resp.status_code == 400
        assert resp.get_json() == {"erro": "Erro"}
