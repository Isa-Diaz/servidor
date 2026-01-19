from unittest.mock import patch
from acesso.controller.cliente_controller import app

def test_criar_cliente_controller_retorna_erro():
    # Força o service retornar string (caminho do erro)
    with patch("acesso.controller.cliente_controller.criar_cliente_service", return_value="erro"):
        client = app.test_client()
        response = client.post("/clientes", json={"qualquer": "dado"})

        assert response.status_code == 400
        assert response.json["erro"] == "erro"

