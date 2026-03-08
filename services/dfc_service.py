from database.db import get_db
from services.dre_service import calcular_dre


def calcular_dfc():
    db = get_db()

    try:

        dre = calcular_dre()

        # ===============================
        # ATIVIDADES OPERACIONAIS
        # ===============================
        operacionais = float(dre.get("lucro_liquido", 0))


        # ===============================
        # ATIVIDADES DE INVESTIMENTO
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
            WHERE c.nome LIKE '%investimento%'
               OR (c.tipo = 'Ativo' AND c.nome NOT LIKE '%circulante%')
        """).fetchone()

        investimento = float(result["total"])


        # ===============================
        # ATIVIDADES DE FINANCIAMENTO
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
            WHERE c.tipo IN ('Passivo', 'Patrimônio Líquido')
        """).fetchone()

        financiamento = float(result["total"])


        # ===============================
        # CÁLCULO FINAL
        # ===============================
        entradas = operacionais + investimento + financiamento
        saidas = 0.0
        saldo_final = entradas - saidas


        return {
            "operacionais": operacionais,
            "investimento": investimento,
            "financiamento": financiamento,
            "entradas": entradas,
            "saidas": saidas,
            "saldo_final": saldo_final
        }

    except Exception as e:

        print("Erro ao calcular DFC:", e)

        return {
            "operacionais": 0,
            "investimento": 0,
            "financiamento": 0,
            "entradas": 0,
            "saidas": 0,
            "saldo_final": 0
        }

    finally:
        db.close()