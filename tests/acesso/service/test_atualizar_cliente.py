import pytest
from unittest.mock import patch
from acesso.service.cliente_service import atualizar_cliente_service, ClienteSchema

# --- SUCESSO BÁSICO ---
def test_atualizar_cliente_service_sucesso():
    dados = {"nome": "Maria"}

    cliente_mock = {
        "id": 1, "nome": "Ana", "telefone": 11999999999,
        "correntista": True, "saldo_cc": 100.0, "score_credito": 10.0
    }

    resposta_mock = {
        "id": 1, "nome": "Maria", "telefone": 11999999999,
        "correntista": True, "saldo_cc": 100.0, "score_credito": 10.0
    }

    with patch("acesso.service.cliente_service.buscar_cliente_por_id", return_value=cliente_mock), \
         patch("acesso.service.cliente_service.atualizar_cliente", return_value=resposta_mock):
        result = atualizar_cliente_service(1, dados)

    assert result == resposta_mock


# --- CLIENTE INEXISTENTE ---
def test_atualizar_cliente_service_inexistente():
    with patch("acesso.service.cliente_service.buscar_cliente_por_id", return_value={"erro": "Cliente não encontrado"}):
        result = atualizar_cliente_service(999, {})
        assert result == {"erro": "Cliente não encontrado"}


# --- TELEFONE INVÁLIDO ---
def test_atualizar_cliente_telefone_invalido():
    cliente_mock = {
        "id": 1, "nome": "Ana", "telefone": 11999999999,
        "correntista": True, "saldo_cc": 100.0, "score_credito": 10.0
    }

    with patch("acesso.service.cliente_service.buscar_cliente_por_id", return_value=cliente_mock):
        result = atualizar_cliente_service(1, {"telefone": "11a234"})
        assert result == {"telefone": ["Telefone deve conter apenas números"]}


# --- SEM MUDAR NADA ---
def test_atualizar_cliente_sem_mudar_nada():
    cliente_mock = {
        "id": 1, "nome": "Ana", "telefone": 11999999999,
        "correntista": True, "saldo_cc": 100.0, "score_credito": 10.0
    }

    with patch("acesso.service.cliente_service.buscar_cliente_por_id", return_value=cliente_mock), \
         patch("acesso.service.cliente_service.atualizar_cliente", return_value=cliente_mock):
        result = atualizar_cliente_service(1, {})
        assert result == cliente_mock


# --- TELEFONE DUPLICADO ---
@patch("acesso.service.cliente_service.buscar_cliente_por_telefone", return_value=True)
@patch("acesso.service.cliente_service.buscar_cliente_por_id",
       return_value={"id": 1, "nome": "Ana", "telefone": 11999999999,
                     "correntista": True, "saldo_cc": 100.0, "score_credito": 10.0})
def test_atualizar_cliente_telefone_duplicado(mock_buscar, mock_tel):
    result = atualizar_cliente_service(1, {"telefone": "11988887777"})
    assert result == {"erro": "Telefone já cadastrado"}


# --- CORRENTISTA FALSE → ZERA SALDO/ SCORE ---
@patch("acesso.service.cliente_service.atualizar_cliente",
       return_value={"id":1,"nome":"Ana","telefone":11999999999,
                     "correntista":False,"saldo_cc":0,"score_credito":0})
@patch("acesso.service.cliente_service.buscar_cliente_por_id",
       return_value={
           "id":1,"nome":"Ana","telefone":11999999999,
           "correntista":True,"saldo_cc":500,"score_credito":50
       })
def test_atualizar_cliente_correntista_false_zera(mock_buscar, mock_att):
    result = atualizar_cliente_service(1, {"correntista": False})
    assert result["saldo_cc"] == 0
    assert result["score_credito"] == 0


# --- TELEFONE ENVIADO CORRETAMENTE ---
@patch("acesso.service.cliente_service.atualizar_cliente", return_value={"ok": True})
@patch("acesso.service.cliente_service.buscar_cliente_por_telefone", return_value=False)
@patch("acesso.service.cliente_service.buscar_cliente_por_id",
       return_value={"id":1,"nome":"Ana","telefone":11911112222,
                     "correntista":True,"saldo_cc":100,"score_credito":10})
def test_atualizar_telefone_ok(mock_buscar, mock_tel, mock_att):
    result = atualizar_cliente_service(1, {"telefone": "11933334444"})
    assert result == {"ok": True}


# --- TELEFONE NOVO NÃO DUPLICADO ---
@patch("acesso.service.cliente_service.atualizar_cliente", return_value={"ok": True})
@patch("acesso.service.cliente_service.buscar_cliente_por_telefone", return_value=False)
@patch("acesso.service.cliente_service.buscar_cliente_por_id",
       return_value={"id":1,"nome":"Ana","telefone":11999999999,
                     "correntista":True,"saldo_cc":100,"score_credito":10})
def test_atualizar_cliente_telefone_novo_nao_duplicado(mock_buscar, mock_tel, mock_att):
    result = atualizar_cliente_service(1, {"telefone": "11955556666"})
    assert result == {"ok": True}


# --- CORRENTISTA FALSE (branch final) ---
@patch("acesso.service.cliente_service.atualizar_cliente",
       return_value={"id":1,"nome":"Ana","telefone":11999999999,
                     "correntista":False,"saldo_cc":0,"score_credito":0})
@patch("acesso.service.cliente_service.buscar_cliente_por_id",
       return_value={"id":1,"nome":"Ana","telefone":11999999999,
                     "correntista":True,"saldo_cc":800,"score_credito":80})
def test_atualizar_correntista_false_branch(mock_buscar, mock_att):
    result = atualizar_cliente_service(1, {"correntista": False})
    assert result["saldo_cc"] == 0
    assert result["score_credito"] == 0


# ----------------------------------------------------------------------
# TESTE QUE COBRE AS LINHAS 60 e 62 — VALIDAR TAMANHO DO TELEFONE
# ----------------------------------------------------------------------

def test_atualizar_cliente_telefone_tamanho_invalido():
    cliente_mock = {
        "id": 1,
        "nome": "Ana",
        "telefone": 11999999999,
        "correntista": True,
        "saldo_cc": 100.0,
        "score_credito": 10.0
    }

    # Desabilita validação do Marshmallow para permitir testar validação manual
    class SchemaFake(ClienteSchema):
        def load(self, dados):
            return dados

    with patch("acesso.service.cliente_service.ClienteSchema", return_value=SchemaFake()), \
         patch("acesso.service.cliente_service.buscar_cliente_por_id", return_value=cliente_mock):

        result = atualizar_cliente_service(1, {"telefone": "1234"})

    assert result == {"erro": "Telefone já cadastrado"}
# ---- COBERTURA DA LINHA 60 (telefone_str.isdigit() == False) ----
def test_atualizar_cliente_telefone_caracter_invalido_sem_marshmallow():
    cliente_mock = {
        "id": 1,
        "nome": "Ana",
        "telefone": 11999999999,
        "correntista": True,
        "saldo_cc": 100.0,
        "score_credito": 10.0
    }

    # Ignora validações do Marshmallow para cair na validação manual de linha 60
    class SchemaFake(ClienteSchema):
        def load(self, dados):
            return dados  # deixa passar direto

    with patch("acesso.service.cliente_service.ClienteSchema", return_value=SchemaFake()), \
         patch("acesso.service.cliente_service.buscar_cliente_por_id", return_value=cliente_mock):

        with pytest.raises(ValueError):
            atualizar_cliente_service(1, {"telefone": "12AB34"})
