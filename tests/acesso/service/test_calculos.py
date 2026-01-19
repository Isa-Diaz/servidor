
from acesso.service.cliente_service import (
    calcular_score,
    calcular_novo_saldo,
    calcular_limite,
)

def test_calcular_score_positivo():
    assert calcular_score(100) == 10
    
def test_calcular_score_zero():
    assert calcular_score(0) == 0

def test_calcular_score_negativo():
    assert calcular_score(-50) == 0

def test_calcular_novo_saldo_deposito():
    assert calcular_novo_saldo(100, "deposito", 50) == 150

def test_calcular_novo_saldo_saque():
    assert calcular_novo_saldo(100, "saque", 50) == 50

def test_calcular_limite():
    assert calcular_limite(10) == 30
