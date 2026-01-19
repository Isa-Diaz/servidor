from unittest.mock import patch, MagicMock
import micro_servico.repository.storage_repository as repo


@patch("micro_servico.repository.storage_repository.connect")
def test_create_table(mock_con):
    conn = MagicMock()
    mock_con.return_value = conn
    repo.create_table()
    conn.cursor.assert_called_once()
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


@patch("micro_servico.repository.storage_repository.connect")
def test_insert_cliente(mock_con):
    conn = MagicMock()
    cursor = MagicMock()
    cursor.lastrowid = 1
    conn.cursor.return_value = cursor
    mock_con.return_value = conn

    out = repo.insert_cliente("Ana", 1, True, 1.0, 10.0)

    assert out == 1
    conn.cursor.assert_called_once()
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


@patch("micro_servico.repository.storage_repository.connect")
def test_listar_clientes(mock_con):
    conn = MagicMock()
    cursor = MagicMock()
    cursor.fetchall.return_value = [(1,)]
    conn.cursor.return_value = cursor
    mock_con.return_value = conn

    result = repo.listar_clientes()

    assert result == [(1,)]
    conn.cursor.assert_called_once()
    conn.close.assert_called_once()


@patch("micro_servico.repository.storage_repository.connect")
def test_buscar_cliente_por_id(mock_con):
    conn = MagicMock()
    cursor = MagicMock()
    cursor.fetchone.return_value = (1, "Ana")
    conn.cursor.return_value = cursor
    mock_con.return_value = conn

    result = repo.buscar_cliente_por_id(1)

    assert result == (1, "Ana")
    conn.cursor.assert_called_once()
    conn.close.assert_called_once()


@patch("micro_servico.repository.storage_repository.connect")
def test_atualizar_cliente(mock_con):
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value = cursor
    mock_con.return_value = conn

    repo.atualizar_cliente(1, "Ana", 1, True, 1.0, 10.0)

    conn.cursor.assert_called_once()
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


@patch("micro_servico.repository.storage_repository.connect")
def test_delete_cliente(mock_con):
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value = cursor
    mock_con.return_value = conn

    repo.delete_cliente(1)

    conn.cursor.assert_called_once()
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


@patch("micro_servico.repository.storage_repository.connect")
def test_buscar_cliente_por_telefone(mock_con):
    conn = MagicMock()
    cursor = MagicMock()
    cursor.fetchone.return_value = ("linha",)
    conn.cursor.return_value = cursor
    mock_con.return_value = conn

    result = repo.buscar_cliente_por_telefone(1234)

    assert result == ("linha",)
    conn.cursor.assert_called_once()
    conn.close.assert_called_once()
