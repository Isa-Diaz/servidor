from unittest.mock import patch
from marshmallow import ValidationError
from acesso.service.cliente_service import processar_dados


# -----------------------------
# LINHA 23 - ValidationError via fluxo normal
# -----------------------------
def test_processar_dados_marshmallow_validation_error():
    out = processar_dados({})
    assert isinstance(out, dict)  # marshmallow retorna dict de erros


# Precisamos impedir o Marshmallow para cair na validação manual
class SchemaFake:
    def load(self, dados):
        # ignora validação automática e apenas devolve os dados
        return dados


# -----------------------------
# LINHA 28 - telefone_str.isdigit() == False
# -----------------------------
@patch("acesso.service.cliente_service.ClienteSchema", return_value=SchemaFake())
def test_processar_dados_telefone_invalido_tipo(_):
    out = processar_dados({
        "nome": "Ana",
        "telefone": "abc",
        "correntista": True,
        "saldo_cc": "10"
    })
    assert out == "Telefone deve conter apenas números"


# -----------------------------
# LINHA 31 - len(telefone_str) inválido
# -----------------------------
@patch("acesso.service.cliente_service.ClienteSchema", return_value=SchemaFake())
def test_processar_dados_telefone_tamanho_invalido(_):
    out = processar_dados({
        "nome": "Ana",
        "telefone": "123",
        "correntista": True,
        "saldo_cc": "10"
    })
    assert out == "Telefone deve ter entre 10 e 11 dígitos"


# -----------------------------
# COBERINDO LINHA 23 DE FORMA DIRETA (ValidationError real)
# -----------------------------
def test_processar_dados_forca_validationerror():
    # Patch correto: substitui ClienteSchema dentro do módulo
    with patch("acesso.service.cliente_service.ClienteSchema") as MockSchema:
        instance = MockSchema.return_value
        instance.load.side_effect = ValidationError({"campo": ["erro"]})

        result = processar_dados({"qualquer": "coisa"})

        assert result == {"campo": ["erro"]}  # cobertura da linha 23
