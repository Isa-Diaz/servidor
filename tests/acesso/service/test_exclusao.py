from unittest.mock import patch
from acesso.service.cliente_service import deletar_cliente_service


def test_deletar_cliente_sucesso():
    cliente_mock = {
        "id": 1, "saldo_cc": 0
    }

    with patch("acesso.service.cliente_service.buscar_cliente_por_id", return_value=cliente_mock), \
         patch("acesso.service.cliente_service.deletar_cliente", return_value={"sucesso": "Cliente deletado"}):

        result = deletar_cliente_service(1)

    assert result == {"sucesso": "Cliente deletado"}


def test_deletar_cliente_saldo_nao_zero():
    cliente_mock = {"id": 1, "saldo_cc": 100}

    with patch("acesso.service.cliente_service.buscar_cliente_por_id", return_value=cliente_mock):
        result = deletar_cliente_service(1)

    assert result == {"erro": "Não é possível excluir conta com saldo diferente de zero."}


def test_deletar_cliente_inexistente():
    with patch("acesso.service.cliente_service.buscar_cliente_por_id", return_value={"erro": "Cliente não encontrado"}):
        result = deletar_cliente_service(999)
        assert result == {"erro": "Cliente não encontrado"}

def test_deletar_cliente_id_invalido():
    with patch("acesso.service.cliente_service.buscar_cliente_por_id", return_value={"erro": "Cliente não encontrado"}):
        result = deletar_cliente_service(None)
        assert result == {"erro": "Cliente não encontrado"}
