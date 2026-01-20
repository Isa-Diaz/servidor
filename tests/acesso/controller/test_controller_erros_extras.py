import pytest
from flask import json
from acesso.controller.cliente_controller import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_criar_cliente_retorna_erro_dict(client, monkeypatch):
    # Força criar_cliente_service retornar um dict com erro
    monkeypatch.setattr(
        "acesso.controller.cliente_controller.criar_cliente_service",
        lambda dados: {"erro": "Erro de teste"}
    )

    response = client.post("/clientes", json={"nome": "Teste", "telefone": "1234567890", "correntista": True, "saldo_cc": 0})
    assert response.status_code == 400
    data = response.get_json()
    assert data["erro"] == "Erro de teste"
