from ..client.client import criar_cliente, atualizar_cliente, buscar_cliente_por_id, deletar_cliente
from micro_servico.repository.storage_repository import buscar_cliente_por_telefone
from marshmallow import ValidationError
from ..validators.cliente_schemas import ClienteSchema

def calcular_score(saldo):
    if saldo > 0:
        return saldo * 0.1
    return 0


def processar_dados(dados):
    schema = ClienteSchema()
    try:
        dados_validados = schema.load(dados)
    except ValidationError as err:
        return err.messages

    telefone_raw = dados_validados["telefone"]
    
    # Se vier lista, corrige
    if isinstance(telefone_raw, list):
        telefone_raw = telefone_raw[0]

    telefone_str = str(telefone_raw)

    if not telefone_str.isdigit():
        return "Telefone deve conter apenas números"

    if len(telefone_str) not in (10, 11):
        return "Telefone deve ter entre 10 e 11 dígitos"

    telefone = int(telefone_str)

    saldo_cc = float(dados_validados["saldo_cc"])

    if buscar_cliente_por_telefone(telefone):
        return "Telefone já cadastrado"

    if dados_validados["correntista"] is False:
        saldo_cc = 0

    score_credito = calcular_score(saldo_cc)

    return {
        "nome": dados_validados["nome"],
        "telefone": telefone,
        "correntista": dados_validados["correntista"],
        "saldo_cc": saldo_cc,
        "score_credito": score_credito
    }


def criar_cliente_service(dados):
    result = processar_dados(dados)
    if isinstance(result, str):
        return result
    return criar_cliente(result)

def atualizar_cliente_service(id, dados):
    cliente = buscar_cliente_por_id(id)
    if "erro" in cliente:
        return cliente

    schema = ClienteSchema(partial=True)
    try:
        dados_validados = schema.load(dados)
    except ValidationError as err:
        return err.messages

    nome = dados_validados.get("nome", cliente["nome"])
    telefone_str = str(dados_validados.get("telefone", cliente["telefone"]))


    if not telefone_str.isdigit():
        return "Telefone deve conter apenas números"
    if len(telefone_str) not in (10, 11):
        return "Telefone deve ter entre 10 e 11 dígitos"

    telefone = int(telefone_str)

    if telefone != cliente["telefone"]:
        if buscar_cliente_por_telefone(telefone):
            return {"erro": "Telefone já cadastrado"}

    correntista = dados_validados.get("correntista", cliente["correntista"])

    saldo = cliente["saldo_cc"]
    score = cliente["score_credito"]

    if correntista is False:
        saldo = 0
        score = 0

    novos_dados = {
        "nome": nome,
        "telefone": telefone,
        "correntista": correntista,
        "saldo_cc": saldo,
        "score_credito": score
    }

    return atualizar_cliente(id, novos_dados)

def calcular_novo_saldo(saldo_atual, tipo, valor):
    if tipo == "deposito":
        return saldo_atual + valor
    return saldo_atual - valor

def calcular_limite(score):
    return score * 3

def validar_operacao(dados):
    tipo = dados.get("tipo")
    valor = dados.get("valor")

    if tipo is None:
        return "O campo tipo é obrigatório"
    if tipo not in ["saque", "deposito"]:
        return "Tipo de operação inválido"

    if valor is None:
        return "O campo valor é obrigatório"

    try:
        valor = float(valor)
    except:
        return "Valor deve ser um número"

    if valor <= 0:
        return "Valor deve ser maior que zero"

    return None

def operacao_service(id, dados):
    result = validar_operacao(dados)
    if result:
        return result

    cliente = buscar_cliente_por_id(id)
    if "erro" in cliente:
        return cliente


    if not cliente["correntista"]:
        return {"erro": "Apenas correntistas podem realizar operações bancárias"}

    tipo = dados["tipo"]
    valor = float(dados["valor"])
    saldo_atual = cliente["saldo_cc"]

    novo_saldo = calcular_novo_saldo(saldo_atual, tipo, valor)
    novo_score = calcular_score(novo_saldo)
    limite = calcular_limite(novo_score)

    if novo_saldo < -limite:
        return "Saldo excede o limite do cheque especial"

    novos_dados = {
        "nome": cliente["nome"],
        "telefone": cliente["telefone"],
        "correntista": cliente["correntista"],
        "saldo_cc": novo_saldo,
        "score_credito": novo_score
    }

    return atualizar_cliente(id, novos_dados)

def deletar_cliente_service(id):
    cliente = buscar_cliente_por_id(id)
    if "erro" in cliente:
        return cliente
    if cliente["saldo_cc"] != 0:
        return {"erro": "Não é possível excluir conta com saldo diferente de zero."}
    return deletar_cliente(id)


