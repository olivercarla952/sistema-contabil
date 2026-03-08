from database.db import get_db

def calcular_balanco():
    db = get_db()

    try:

        # ===============================
        # ATIVO
        # ===============================
        result = db.execute("""
            SELECT COALESCE(SUM(
                CASE 
                    WHEN l.tipo = 'Débito' THEN l.valor
                    ELSE -l.valor
                END
            ),0) AS total
            FROM lancamentos l
            JOIN contas c ON l.conta_id = c.id
            WHERE c.tipo = 'Ativo'
        """).fetchone()

        ativo = float(result["total"])


        # ===============================
        # PASSIVO
        # ===============================
        result = db.execute("""
            SELECT COALESCE(SUM(
                CASE 
                    WHEN l.tipo = 'Crédito' THEN l.valor
                    ELSE -l.valor
                END
            ),0) AS total
            FROM lancamentos l
            JOIN contas c ON l.conta_id = c.id
            WHERE c.tipo = 'Passivo'
        """).fetchone()

        passivo = float(result["total"])


        # ===============================
        # PATRIMÔNIO LÍQUIDO (contas)
        # ===============================
        result = db.execute("""
            SELECT COALESCE(SUM(
                CASE 
                    WHEN l.tipo = 'Crédito' THEN l.valor
                    ELSE -l.valor
                END
            ),0) AS total
            FROM lancamentos l
            JOIN contas c ON l.conta_id = c.id
            WHERE c.tipo = 'Patrimônio Líquido'
        """).fetchone()

        patrimonio_conta = float(result["total"])


        # ===============================
        # RECEITAS
        # ===============================
        result = db.execute("""
            SELECT COALESCE(SUM(
                CASE 
                    WHEN l.tipo = 'Crédito' THEN l.valor
                    ELSE -l.valor
                END
            ),0) AS total
            FROM lancamentos l
            JOIN contas c ON l.conta_id = c.id
            WHERE c.tipo = 'Receita'
        """).fetchone()

        receita = float(result["total"])


        # ===============================
        # DESPESAS
        # ===============================
        result = db.execute("""
            SELECT COALESCE(SUM(
                CASE 
                    WHEN l.tipo = 'Débito' THEN l.valor
                    ELSE -l.valor
                END
            ),0) AS total
            FROM lancamentos l
            JOIN contas c ON l.conta_id = c.id
            WHERE c.tipo = 'Despesa'
        """).fetchone()

        despesa = float(result["total"])


        # ===============================
        # CÁLCULO FINAL DO PATRIMÔNIO
        # ===============================
        patrimonio = patrimonio_conta + receita - despesa


        # ===============================
        # VALIDAÇÃO CONTÁBIL
        # ===============================
        validacao = abs(ativo - (passivo + patrimonio)) < 0.01


        return {
            "ativo": ativo,
            "passivo": passivo,
            "patrimonio": patrimonio,
            "validacao": validacao
        }

    except Exception as e:

        print("Erro ao calcular balanço:", e)

        return {
            "ativo": 0,
            "passivo": 0,
            "patrimonio": 0,
            "validacao": False
        }

    finally:
        db.close()