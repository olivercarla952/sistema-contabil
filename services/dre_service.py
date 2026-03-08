from database.db import get_db


def calcular_dre():
    db = get_db()

    try:

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
        # CUSTOS
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
            WHERE c.tipo = 'Custo'
        """).fetchone()

        custo = float(result["total"])


        # ===============================
        # CÁLCULOS DRE
        # ===============================
        receita_bruta = receita
        deducoes = 0.0
        receita_liquida = receita_bruta - deducoes

        lucro_bruto = receita_liquida - custo
        despesas_operacionais = despesa

        lucro_operacional = lucro_bruto - despesas_operacionais
        lucro_liquido = lucro_operacional


        return {
            "receita_bruta": receita_bruta,
            "deducoes": deducoes,
            "receita_liquida": receita_liquida,
            "custos": custo,
            "lucro_bruto": lucro_bruto,
            "despesas_operacionais": despesas_operacionais,
            "lucro_operacional": lucro_operacional,
            "lucro_liquido": lucro_liquido
        }

    except Exception as e:

        print("Erro ao calcular DRE:", e)

        return {
            "receita_bruta": 0,
            "deducoes": 0,
            "receita_liquida": 0,
            "custos": 0,
            "lucro_bruto": 0,
            "despesas_operacionais": 0,
            "lucro_operacional": 0,
            "lucro_liquido": 0
        }

    finally:
        db.close()