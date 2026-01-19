
from acesso.service.cliente_service import validar_operacao

def test_validar_operacao_tipo_ausente():
    assert validar_operacao({"valor": 10}) == "O campo tipo é obrigatório"

def test_validar_operacao_tipo_invalido():
    assert validar_operacao({"tipo": "pix", "valor": 10}) == "Tipo de operação inválido"

def test_validar_operacao_valor_ausente():
    assert validar_operacao({"tipo": "deposito"}) == "O campo valor é obrigatório"

def test_validar_operacao_valor_invalido():
    assert validar_operacao({"tipo": "deposito", "valor": "abc"}) == "Valor deve ser um número"

def test_validar_operacao_valor_negativo():
    assert validar_operacao({"tipo": "saque", "valor": -10}) == "Valor deve ser maior que zero"

def test_validar_operacao_ok():
    assert validar_operacao({"tipo": "deposito", "valor": 10}) is None
