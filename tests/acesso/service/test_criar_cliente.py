from unittest.mock import patch
from acesso.service.cliente_service import criar_cliente_service


def test_criar_cliente_service_sucesso():
    dados = {
        "nome": "Ana",
        "telefone": "11999999999",
        "correntista": True,
        "saldo_cc": "100"
    }

    resposta_mock = {
        "id": 1,
        "nome": "Ana",
        "telefone": 11999999999,
        "correntista": True,
        "saldo_cc": 100.0,
        "score_credito": 10.0
    }

    with patch(
        "acesso.service.cliente_service.processar_dados",
        return_value={"valido": True, "dados": resposta_mock}
    ), patch(
        "acesso.service.cliente_service.criar_cliente",
        return_value=resposta_mock
    ):
        assert criar_cliente_service(dados) == resposta_mock


def test_criar_cliente_service_dados_invalidos():
    with patch("acesso.service.cliente_service.processar_dados", return_value={
    "valido": False,
    "erro": "Erro"
}):
        assert criar_cliente_service({}) == {"erro": "Erro"}

