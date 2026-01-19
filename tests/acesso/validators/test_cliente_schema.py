from marshmallow import ValidationError
from acesso.validators.cliente_schemas import ClienteSchema


def test_schema_sucesso():
    schema = ClienteSchema()
    out = schema.load({
        "nome": "Ana",
        "telefone": "11999999999",
        "correntista": True,
        "saldo_cc": 10
    })
    assert out["telefone"] == "11999999999"


def test_schema_telefone_invalido():
    schema = ClienteSchema()
    try:
        schema.load({
            "nome": "Ana",
            "telefone": "1199A",
            "correntista": True,
            "saldo_cc": 10
        })
    except ValidationError as err:
        assert "telefone" in err.messages


def test_schema_telefone_tamanho():
    schema = ClienteSchema()
    try:
        schema.load({
            "nome": "Ana",
            "telefone": "123",
            "correntista": True,
            "saldo_cc": 10
        })
    except ValidationError as err:
        assert "telefone" in err.messages
