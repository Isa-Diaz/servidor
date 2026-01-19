from acesso.controller.cliente_controller import app
from unittest.mock import patch

def test_listar_clientes_controller_cobertura():
    with patch("acesso.controller.cliente_controller.listar_clientes", return_value=[]):
        client = app.test_client()
        response = client.get("/clientes")
        assert response.status_code == 200
