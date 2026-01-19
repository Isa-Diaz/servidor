from micro_servico.database.db import connect

def create_table():
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefone TEXT,
            correntista BOOLEAN,
            score_credito REAL,
            saldo_cc REAL
        )
    """)

    conexao.commit()
    conexao.close()

def insert_cliente(nome, telefone, correntista, score_credito, saldo_cc):
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute(
        """INSERT INTO pessoas (nome, telefone, correntista, score_credito, saldo_cc)
           VALUES (?, ?, ?, ?, ?)""",
        (nome, telefone, correntista, score_credito, saldo_cc)
    )
    conexao.commit()
    cliente_id = cursor.lastrowid
    conexao.close()
    return cliente_id

def listar_clientes():
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM pessoas")
    linhas = cursor.fetchall()

    conexao.close()
    return linhas

def buscar_cliente_por_id(id):
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM pessoas WHERE id = ?", (id,))
    linha = cursor.fetchone()

    conexao.close()
    return linha

def atualizar_cliente(id, nome, telefone, correntista, score_credito, saldo_cc):
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE pessoas
        SET nome = ?, telefone = ?, correntista = ?, score_credito = ?, saldo_cc = ?
        WHERE id = ?
        """,
        (nome, telefone, correntista, score_credito, saldo_cc, id)
    )

    conexao.commit()
    conexao.close()

def delete_cliente(id):
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM pessoas WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()

def buscar_cliente_por_telefone(telefone):
    conexao = connect()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM pessoas WHERE telefone = ?", (telefone,))
    linha = cursor.fetchone()

    conexao.close()
    return linha
