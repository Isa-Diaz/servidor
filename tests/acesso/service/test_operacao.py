
from unittest.mock import patch
from acesso.service.cliente_service import operacao_service


def test_operacao_deposito_sucesso():
    cliente_mock = {
        "id": 1, "nome": "Isa", "telefone": 11999999999,
        "correntista": True, "score_credito": 10.0, "saldo_cc": 100.0
    }

    resposta_mock = {
        "id": 1, "nome": "Isa", "telefone": 11999999999,
        "correntista": True, "saldo_cc": 150.0, "score_credito": 15.0
    }

    with patch("acesso.service.cliente_service.buscar_cliente_por_id", return_value=cliente_mock), \
         patch("acesso.service.cliente_service.atualizar_cliente", return_value=resposta_mock):
        result = operacao_service(1, {"tipo": "deposito", "valor": 50})

    assert result == resposta_mock


def test_operacao_limite_excedido():
    cliente_mock = {
        "id": 1, "nome": "Ana", "telefone": 11999999999,
        "correntista": True, "saldo_cc": -200.0, "score_credito": 0
    }

    with patch("acesso.service.cliente_service.buscar_cliente_por_id", return_value=cliente_mock):
        result = operacao_service(1, {"tipo": "saque", "valor": 50})

    assert result == "Saldo excede o limite do cheque especial"


def test_operacao_cliente_inexistente():
    with patch("acesso.service.cliente_service.buscar_cliente_por_id", return_value={"erro": "Cliente não encontrado"}):
        result = operacao_service(999, {"tipo": "deposito", "valor": 10})

    assert result == {"erro": "Cliente não encontrado"}


def test_operacao_correntista_false():
    cliente_mock = {"id": 1, "correntista": False}

    with patch("acesso.service.cliente_service.buscar_cliente_por_id", return_value=cliente_mock):
        result = operacao_service(1, {"tipo": "deposito", "valor": 50})

    assert result == {"erro": "Apenas correntistas podem realizar operações bancárias"}

def test_operacao_service_valor_invalido():
    result = operacao_service(1, {"tipo": "deposito", "valor": "abc"})
    assert result == "Valor deve ser um número"
