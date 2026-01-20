from unittest.mock import patch
from marshmallow import ValidationError
from acesso.service.cliente_service import processar_dados

def test_processar_dados_marshmallow_validation_error():
    out = processar_dados({})
    assert isinstance(out, dict)


class SchemaFake:
    def load(self, dados):
        return dados


@patch("acesso.service.cliente_service.ClienteSchema", return_value=SchemaFake())
def test_processar_dados_telefone_invalido_tipo(_):
    out = processar_dados({
        "nome": "Ana",
        "telefone": "abc",
        "correntista": True,
        "saldo_cc": "10"
    })
    assert out["erro"] == "Telefone deve conter apenas números"
    assert out["valido"] is False



@patch("acesso.service.cliente_service.ClienteSchema", return_value=SchemaFake())
def test_processar_dados_telefone_tamanho_invalido(_):
    out = processar_dados({
        "nome": "Ana",
        "telefone": "123",
        "correntista": True,
        "saldo_cc": "10"
    })
    assert out["erro"] == "Telefone deve ter entre 10 e 11 dígitos"
    assert out["valido"] is False



def test_processar_dados_forca_validationerror():
    with patch("acesso.service.cliente_service.ClienteSchema") as MockSchema:
        instance = MockSchema.return_value
        instance.load.side_effect = ValidationError({"campo": ["erro"]})

        result = processar_dados({"x": 1})

        assert result["erro"] == {"campo": ["erro"]}
        assert result["valido"] is False
