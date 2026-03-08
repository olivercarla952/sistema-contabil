from flask import Blueprint, render_template
from services.balanco_service import calcular_balanco
from services.dre_service import calcular_dre
from services.dfc_service import calcular_dfc


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():

    try:

        balanco = calcular_balanco()
        dre = calcular_dre()
        dfc = calcular_dfc()

        indicadores = {
            "receita_total": dre.get("receita_bruta", 0),
            "despesas_totais": dre.get("despesas_operacionais", 0),
            "lucro_liquido": dre.get("lucro_liquido", 0),
            "ativo_total": balanco.get("ativo", 0),
            "passivo_total": balanco.get("passivo", 0),
            "patrimonio_liquido": balanco.get("patrimonio", 0),
            "saldo_caixa": dfc.get("saldo_final", 0)
        }

        return render_template(
            "dashboard.html",
            indicadores=indicadores
        )

    except Exception as e:

        print("Erro ao carregar dashboard:", e)

        indicadores = {
            "receita_total": 0,
            "despesas_totais": 0,
            "lucro_liquido": 0,
            "ativo_total": 0,
            "passivo_total": 0,
            "patrimonio_liquido": 0,
            "saldo_caixa": 0
        }

        return render_template(
            "dashboard.html",
            indicadores=indicadores
        )