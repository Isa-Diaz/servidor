from acesso.service.cliente_service import processar_dados
import pytest

def test_processar_dados_saldo_negativo():
    dados = {
        "nome": "Teste",
        "telefone": "11999999999",
        "correntista": True,
        "saldo_cc": -100  # aqui forçamos o saldo negativo
    }

    resultado = processar_dados(dados)
    
    assert resultado["valido"] is False
    assert resultado["erro"] == "Saldo inicial não pode ser negativo"
