class Lancamento:

    def __init__(self, id=None, data=None, conta_id=None, descricao=None, tipo=None, valor=0.0, conta_nome=None):
        self.id = id
        self.data = data
        self.conta_id = conta_id
        self.descricao = descricao
        self.tipo = tipo
        self.valor = valor
        self.conta_nome = conta_nome


    # ===============================
    # BUSCAR TODOS OS LANÇAMENTOS
    # ===============================
    @staticmethod
    def get_all():

        from database.db import get_lancamentos

        try:

            rows = get_lancamentos()

            return [
                Lancamento(
                    id=row["id"],
                    data=row["data"],
                    conta_id=row["conta_id"],
                    descricao=row["descricao"],
                    tipo=row["tipo"],
                    valor=row["valor"],
                    conta_nome=row.get("conta_nome")
                )
                for row in rows
            ]

        except Exception as e:

            print("Erro ao buscar lançamentos:", e)
            return []


    # ===============================
    # BUSCAR POR ID
    # ===============================
    @staticmethod
    def get_by_id(lancamento_id):

        from database.db import get_db

        db = get_db()

        try:

            row = db.execute(
                """
                SELECT l.*, c.nome AS conta_nome
                FROM lancamentos l
                JOIN contas c ON l.conta_id = c.id
                WHERE l.id = ?
                """,
                (lancamento_id,)
            ).fetchone()

            if row:

                return Lancamento(
                    id=row["id"],
                    data=row["data"],
                    conta_id=row["conta_id"],
                    descricao=row["descricao"],
                    tipo=row["tipo"],
                    valor=row["valor"],
                    conta_nome=row["conta_nome"]
                )

            return None

        except Exception as e:

            print("Erro ao buscar lançamento:", e)
            return None

        finally:
            db.close()


    # ===============================
    # SALVAR NOVO LANÇAMENTO
    # ===============================
    def save(self):

        from database.db import insert_lancamento

        try:

            insert_lancamento(
                self.data,
                self.conta_id,
                self.descricao,
                self.tipo,
                self.valor
            )

        except Exception as e:

            print("Erro ao salvar lançamento:", e)


    # ===============================
    # ATUALIZAR LANÇAMENTO
    # ===============================
    def update(self):

        from database.db import update_lancamento

        try:

            update_lancamento(
                self.id,
                self.data,
                self.conta_id,
                self.descricao,
                self.tipo,
                self.valor
            )

        except Exception as e:

            print("Erro ao atualizar lançamento:", e)


    # ===============================
    # DELETAR LANÇAMENTO
    # ===============================
    @staticmethod
    def delete(lancamento_id):

        from database.db import delete_lancamento

        try:

            delete_lancamento(lancamento_id)

        except Exception as e:

            print("Erro ao deletar lançamento:", e)