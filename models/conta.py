class Conta:

    def __init__(self, id=None, codigo=None, nome=None, tipo=None):
        self.id = id
        self.codigo = codigo
        self.nome = nome
        self.tipo = tipo


    # ===============================
    # BUSCAR TODAS AS CONTAS
    # ===============================
    @staticmethod
    def get_all():
        from database.db import get_contas

        try:

            contas = get_contas()

            return [
                Conta(
                    id=row["id"],
                    codigo=row["codigo"],
                    nome=row["nome"],
                    tipo=row["tipo"]
                )
                for row in contas
            ]

        except Exception as e:
            print("Erro ao buscar contas:", e)
            return []


    # ===============================
    # BUSCAR CONTA POR ID
    # ===============================
    @staticmethod
    def get_by_id(conta_id):
        from database.db import get_db

        db = get_db()

        try:

            row = db.execute(
                "SELECT * FROM contas WHERE id = ?",
                (conta_id,)
            ).fetchone()

            if row:

                return Conta(
                    id=row["id"],
                    codigo=row["codigo"],
                    nome=row["nome"],
                    tipo=row["tipo"]
                )

            return None

        except Exception as e:

            print("Erro ao buscar conta:", e)
            return None

        finally:
            db.close()


    # ===============================
    # SALVAR NOVA CONTA
    # ===============================
    def save(self):

        from database.db import insert_conta

        try:

            insert_conta(
                self.codigo,
                self.nome,
                self.tipo
            )

        except Exception as e:

            print("Erro ao salvar conta:", e)


    # ===============================
    # ATUALIZAR CONTA
    # ===============================
    def update(self):

        from database.db import get_db

        db = get_db()

        try:

            db.execute(
                """
                UPDATE contas
                SET codigo = ?, nome = ?, tipo = ?
                WHERE id = ?
                """,
                (self.codigo, self.nome, self.tipo, self.id)
            )

            db.commit()

        except Exception as e:

            print("Erro ao atualizar conta:", e)

        finally:
            db.close()


    # ===============================
    # DELETAR CONTA
    # ===============================
    @staticmethod
    def delete(conta_id):

        from database.db import get_db

        db = get_db()

        try:

            db.execute(
                "DELETE FROM contas WHERE id = ?",
                (conta_id,)
            )

            db.commit()

        except Exception as e:

            print("Erro ao deletar conta:", e)

        finally:
            db.close()