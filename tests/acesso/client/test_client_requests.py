import requests
from unittest.mock import patch
from acesso.client.client import (
    listar_clientes,
    buscar_cliente_por_id,
    criar_cliente,
    atualizar_cliente,
    deletar_cliente
)


@patch("requests.get")
def test_listar_clientes(mock_get):
    mock_get.return_value.json.return_value = [{"id": 1}]
    assert listar_clientes() == [{"id": 1}]
    mock_get.assert_called_once()


@patch("requests.get")
def test_buscar_cliente_por_id(mock_get):
    mock_get.return_value.json.return_value = {"id": 1}
    assert buscar_cliente_por_id(1) == {"id": 1}
    mock_get.assert_called_once()


@patch("requests.post")
def test_criar_cliente(mock_post):
    mock_post.return_value.json.return_value = {"ok": True}
    assert criar_cliente({"a": 1}) == {"ok": True}
    mock_post.assert_called_once()


@patch("requests.put")
def test_atualizar_cliente(mock_put):
    mock_put.return_value.json.return_value = {"ok": True}
    assert atualizar_cliente(1, {"a": 1}) == {"ok": True}
    mock_put.assert_called_once()


@patch("requests.delete")
def test_deletar_cliente(mock_delete):
    mock_delete.return_value.json.return_value = {"deleted": True}
    assert deletar_cliente(1) == {"deleted": True}
    mock_delete.assert_called_once()
