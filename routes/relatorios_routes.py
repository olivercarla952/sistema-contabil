from flask import Blueprint, render_template, flash
from services.balanco_service import calcular_balanco
from services.dre_service import calcular_dre
from services.dfc_service import calcular_dfc
from services.dva_service import calcular_dva


relatorios_bp = Blueprint("relatorios", __name__, url_prefix="/relatorios")


# ===============================
# BALANÇO PATRIMONIAL
# ===============================
@relatorios_bp.route("/balanco")
def balanco():

    try:
        data = calcular_balanco()
    except Exception as e:
        print("Erro ao gerar balanço:", e)
        flash("Erro ao gerar Balanço Patrimonial.", "error")
        data = {}

    return render_template("balanco.html", data=data)


# ===============================
# DRE
# ===============================
@relatorios_bp.route("/dre")
def dre():

    try:
        data = calcular_dre()
    except Exception as e:
        print("Erro ao gerar DRE:", e)
        flash("Erro ao gerar DRE.", "error")
        data = {}

    return render_template("dre.html", data=data)


# ===============================
# DFC
# ===============================
@relatorios_bp.route("/dfc")
def dfc():

    try:
        data = calcular_dfc()
    except Exception as e:
        print("Erro ao gerar DFC:", e)
        flash("Erro ao gerar Demonstração de Fluxo de Caixa.", "error")
        data = {}

    return render_template("dfc.html", data=data)


# ===============================
# DVA
# ===============================
@relatorios_bp.route("/dva")
def dva():

    try:
        data = calcular_dva()
    except Exception as e:
        print("Erro ao gerar DVA:", e)
        flash("Erro ao gerar Demonstração do Valor Adicionado.", "error")
        data = {}

    return render_template("dva.html", data=data)