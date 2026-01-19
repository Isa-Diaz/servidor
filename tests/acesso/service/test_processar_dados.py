from unittest.mock import patch
from acesso.service.cliente_service import processar_dados


def test_processar_dados_sucesso():
    dados = {
        "nome": "Ana",
        "telefone": "11999999999",
        "correntista": True,
        "saldo_cc": "100"
    }

    with patch("acesso.service.cliente_service.buscar_cliente_por_telefone", return_value=None):
        result = processar_dados(dados)

    assert result["nome"] == "Ana"
    assert result["telefone"] == 11999999999
    assert result["saldo_cc"] == 100.0
    assert result["score_credito"] == 10.0


def test_processar_dados_telefone_duplicado():
    dados = {
        "nome": "Ana",
        "telefone": "11999999999",
        "correntista": True,
        "saldo_cc": "100"
    }

    with patch("acesso.service.cliente_service.buscar_cliente_por_telefone", return_value=True):
        result = processar_dados(dados)

    assert result == "Telefone já cadastrado"


def test_processar_dados_correntista_false_zera_saldo():
    dados = {
        "nome": "Ana",
        "telefone": "11999999999",
        "correntista": False,
        "saldo_cc": "500"
    }

    with patch("acesso.service.cliente_service.buscar_cliente_por_telefone", return_value=None):
        result = processar_dados(dados)

    assert result["saldo_cc"] == 0
    assert result["score_credito"] == 0


# ---- COBERTURA DAS LINHAS 16-17 / 23 / 26 ----
@patch("micro_servico.repository.storage_repository.buscar_cliente_por_telefone", return_value=None)
@patch("acesso.service.cliente_service.buscar_cliente_por_telefone", return_value=None)
def test_processar_dados_fluxo_valido_sem_duplicidade(mock_repo, mock_local):
    dados = {
        "nome": "Carla",
        "telefone": "11000000000",
        "correntista": True,
        "saldo_cc": "250"
    }

    result = processar_dados(dados)

    assert result["telefone"] == 11000000000
    assert result["saldo_cc"] == 250.0
    assert result["score_credito"] == 25.0


# ---- ERRO DO MARSHMALLOW ----
@patch("micro_servico.repository.storage_repository.buscar_cliente_por_telefone", return_value=None)
@patch("acesso.service.cliente_service.buscar_cliente_por_telefone", return_value=None)
def test_processar_dados_marshmallow_erro(mock_repo, mock_local):
    dados = {
        "nome": "",
        "telefone": "11988887777",
        "correntista": True,
        "saldo_cc": "100"
    }

    result = processar_dados(dados)

    assert "nome" in result

def test_processar_dados_marshmallow_erro_telefone_invalido():
    dados = {
        "nome": "Ana",
        "telefone": "abc123",   # força ValidationError
        "correntista": True,
        "saldo_cc": "100"
    }
    result = processar_dados(dados)
    assert "telefone" in result
