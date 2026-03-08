from database.db import get_db
from services.dre_service import calcular_dre


def calcular_dva():
    db = get_db()

    try:

        dre = calcular_dre()

        # ===============================
        # VALOR ADICIONADO
        # ===============================
        receita_bruta = float(dre.get("receita_bruta", 0))
        custos = float(dre.get("custos", 0))

        va = receita_bruta - custos


        # ===============================
        # FUNCIONÁRIOS
        # ===============================
        result = db.execute("""
            SELECT COALESCE(SUM(l.valor),0) AS total
            FROM lancamentos l
            JOIN contas c ON l.conta_id = c.id
            WHERE (c.nome LIKE '%salario%' OR c.nome LIKE '%funcionario%')
            AND l.tipo = 'Débito'
        """).fetchone()

        funcionarios = float(result["total"]) if result["total"] else (va * 0.5)


        # ===============================
        # GOVERNO
        # ===============================
        result = db.execute("""
            SELECT COALESCE(SUM(l.valor),0) AS total
            FROM lancamentos l
            JOIN contas c ON l.conta_id = c.id
            WHERE (c.nome LIKE '%imposto%' OR c.nome LIKE '%governo%')
            AND l.tipo = 'Débito'
        """).fetchone()

        governo = float(result["total"]) if result["total"] else (va * 0.2)


        # ===============================
        # FINANCIADORES
        # ===============================
        result = db.execute("""
            SELECT COALESCE(SUM(l.valor),0) AS total
            FROM lancamentos l
            JOIN contas c ON l.conta_id = c.id
            WHERE (c.nome LIKE '%juros%' OR c.nome LIKE '%financiamento%')
            AND l.tipo = 'Débito'
        """).fetchone()

        financiadores = float(result["total"]) if result["total"] else (va * 0.1)


        # ===============================
        # SÓCIOS
        # ===============================
        socios = va - funcionarios - governo - financiadores


        return {
            "valor_adicionado": va,
            "funcionarios": funcionarios,
            "governo": governo,
            "financiadores": financiadores,
            "socios": socios
        }

    except Exception as e:

        print("Erro ao calcular DVA:", e)

        return {
            "valor_adicionado": 0,
            "funcionarios": 0,
            "governo": 0,
            "financiadores": 0,
            "socios": 0
        }

    finally:
        db.close()