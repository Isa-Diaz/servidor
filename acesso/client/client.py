
import requests

url_acess = "http://localhost:5000/"
endpoint_base = "clientes"

def listar_clientes():
    url_nova = url_acess + endpoint_base
    result = requests.get(url_nova)
    try:
        return result.json()
    except ValueError:
        return {"erro": "Resposta inválida do microserviço", "raw": result.text}


def buscar_cliente_por_id(id):
    id = str(id)
    url_nova = url_acess + endpoint_base + "/" + id
    result = requests.get(url_nova)
    try:
        return result.json()
    except ValueError:
        return {"erro": "Resposta inválida do microserviço", "raw": result.text}


def criar_cliente(dados):
    url_nova = url_acess + endpoint_base
    result = requests.post(url_nova, json=dados)
    try:
        return result.json()
    except ValueError:
        return {"erro": "Resposta inválida do microserviço", "raw": result.text}


def atualizar_cliente(id, dados):
    id = str(id)
    url_nova = url_acess + endpoint_base + "/" + id
    result = requests.put(url_nova, json=dados)
    try:
        return result.json()
    except ValueError:
        return {"erro": "Resposta inválida do microserviço", "raw": result.text}


def deletar_cliente(id):
    id = str(id)
    url_nova = url_acess + endpoint_base + "/" + id
    result = requests.delete(url_nova)
    try:
        return result.json()
    except ValueError:
        return {"erro": "Resposta inválida do microserviço", "raw": result.text}
