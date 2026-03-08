import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), "sistema_contabil.db")


# ===============================
# CONEXÃO COM BANCO
# ===============================
def get_db():
    try:
        db = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        return db
    except sqlite3.Error as e:
        raise Exception(f"Erro ao conectar ao banco de dados: {e}")


# ===============================
# INICIALIZAR BANCO
# ===============================
def init_db():

    db = get_db()

    try:

        # TABELA CONTAS
        db.execute("""
        CREATE TABLE IF NOT EXISTS contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
        """)

        # TABELA LANÇAMENTOS
        db.execute("""
        CREATE TABLE IF NOT EXISTS lancamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            conta_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL,
            FOREIGN KEY (conta_id) REFERENCES contas(id)
        )
        """)

        # CONTAS PADRÃO
        contas_padrao = [
            ("1.1.1", "Caixa", "Ativo"),
            ("1.1.2", "Banco", "Ativo"),
            ("2.1.1", "Fornecedores", "Passivo"),
            ("3.1.1", "Capital Social", "Patrimônio Líquido"),
            ("4.1.1", "Receita de Vendas", "Receita"),
            ("5.1.1", "Salários", "Despesa"),
            ("6.1.1", "Custos de Produção", "Custo")
        ]

        for codigo, nome, tipo in contas_padrao:

            db.execute("""
            INSERT OR IGNORE INTO contas (codigo, nome, tipo)
            VALUES (?, ?, ?)
            """, (codigo, nome, tipo))

        db.commit()

    except sqlite3.Error as e:

        raise Exception(f"Erro ao inicializar banco de dados: {e}")

    finally:
        db.close()


# ===============================
# CONTAS
# ===============================
def insert_conta(codigo, nome, tipo):

    db = get_db()

    try:

        db.execute("""
        INSERT INTO contas (codigo, nome, tipo)
        VALUES (?, ?, ?)
        """, (codigo, nome, tipo))

        db.commit()

    except sqlite3.Error as e:

        raise Exception(f"Erro ao inserir conta: {e}")

    finally:
        db.close()


def get_contas():

    db = get_db()

    try:

        contas = db.execute("""
        SELECT * FROM contas
        ORDER BY codigo
        """).fetchall()

        return contas

    except sqlite3.Error as e:

        raise Exception(f"Erro ao buscar contas: {e}")

    finally:
        db.close()


# ===============================
# LANÇAMENTOS
# ===============================
def insert_lancamento(data, conta_id, descricao, tipo, valor):

    db = get_db()

    try:

        db.execute("""
        INSERT INTO lancamentos (data, conta_id, descricao, tipo, valor)
        VALUES (?, ?, ?, ?, ?)
        """, (data, conta_id, descricao, tipo, valor))

        db.commit()

    except sqlite3.Error as e:

        raise Exception(f"Erro ao inserir lançamento: {e}")

    finally:
        db.close()


def get_lancamentos():

    db = get_db()

    try:

        lancamentos = db.execute("""
        SELECT 
            l.*,
            c.nome AS conta_nome
        FROM lancamentos l
        JOIN contas c ON l.conta_id = c.id
        ORDER BY l.data DESC
        """).fetchall()

        return lancamentos

    except sqlite3.Error as e:

        raise Exception(f"Erro ao buscar lançamentos: {e}")

    finally:
        db.close()


def update_lancamento(id, data, conta_id, descricao, tipo, valor):

    db = get_db()

    try:

        db.execute("""
        UPDATE lancamentos
        SET data = ?, conta_id = ?, descricao = ?, tipo = ?, valor = ?
        WHERE id = ?
        """, (data, conta_id, descricao, tipo, valor, id))

        db.commit()

    except sqlite3.Error as e:

        raise Exception(f"Erro ao atualizar lançamento: {e}")

    finally:
        db.close()


def delete_lancamento(id):

    db = get_db()

    try:

        db.execute("""
        DELETE FROM lancamentos
        WHERE id = ?
        """, (id,))

        db.commit()

    except sqlite3.Error as e:

        raise Exception(f"Erro ao deletar lançamento: {e}")

    finally:
        db.close()