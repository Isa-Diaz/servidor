from marshmallow import Schema, fields, validates, ValidationError

class ClienteSchema(Schema):
    nome = fields.String(required=True)
    telefone = fields.String(required=True)
    correntista = fields.Boolean(required=True)
    saldo_cc = fields.Float(required=True)

    @validates("telefone")
    def validar_telefone(self, value, **kwargs):
        if not value.isdigit():
            raise ValidationError("Telefone deve conter apenas números")

        if len(value) not in (10, 11):
            raise ValidationError("Telefone deve ter entre 10 e 11 dígitos")
