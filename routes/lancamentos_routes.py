from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.lancamento import Lancamento
from models.conta import Conta
from datetime import datetime


lancamentos_bp = Blueprint("lancamentos", __name__, url_prefix="/lancamentos")


# ===============================
# LISTAR LANÇAMENTOS
# ===============================
@lancamentos_bp.route("/")
def index():

    try:
        lancamentos = Lancamento.get_all()
        contas = Conta.get_all()

        return render_template(
            "lancamentos.html",
            lancamentos=lancamentos,
            contas=contas
        )

    except Exception as e:
        print("Erro ao carregar lançamentos:", e)
        flash("Erro ao carregar lançamentos.", "error")
        return render_template(
            "lancamentos.html",
            lancamentos=[],
            contas=[]
        )


# ===============================
# ADICIONAR LANÇAMENTO
# ===============================
@lancamentos_bp.route("/add", methods=["POST"])
def add():

    data = request.form.get("data")
    conta_id_str = request.form.get("conta_id")
    descricao = request.form.get("descricao")
    tipo = request.form.get("tipo")
    valor_str = request.form.get("valor")

    # Validação de campos obrigatórios
    if not all([data, conta_id_str, descricao, tipo, valor_str]):
        flash("Todos os campos são obrigatórios.", "error")
        return redirect(url_for("lancamentos.index"))

    # Validação de conta_id e valor
    try:
        conta_id = int(conta_id_str)
        valor = float(valor_str)

        if valor <= 0:
            raise ValueError

    except ValueError:
        flash("Valor deve ser um número positivo.", "error")
        return redirect(url_for("lancamentos.index"))

    # Validação de data
    try:
        datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        flash("Data inválida. Use formato YYYY-MM-DD.", "error")
        return redirect(url_for("lancamentos.index"))

    # Validação tipo
    if tipo not in ["Débito", "Crédito"]:
        flash("Tipo deve ser Débito ou Crédito.", "error")
        return redirect(url_for("lancamentos.index"))

    try:

        lancamento = Lancamento(
            data=data,
            conta_id=conta_id,
            descricao=descricao,
            tipo=tipo,
            valor=valor
        )

        lancamento.save()

        flash("Lançamento adicionado com sucesso.", "success")

    except Exception as e:

        print("Erro ao salvar lançamento:", e)
        flash("Erro ao salvar lançamento.", "error")

    return redirect(url_for("lancamentos.index"))


# ===============================
# EDITAR LANÇAMENTO
# ===============================
@lancamentos_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    lancamento = Lancamento.get_by_id(id)

    if lancamento is None:
        flash("Lançamento não encontrado.", "error")
        return redirect(url_for("lancamentos.index"))

    if request.method == "POST":

        data = request.form.get("data")
        conta_id_str = request.form.get("conta_id")
        descricao = request.form.get("descricao")
        tipo = request.form.get("tipo")
        valor_str = request.form.get("valor")

        if not all([data, conta_id_str, descricao, tipo, valor_str]):
            flash("Todos os campos são obrigatórios.", "error")
            return redirect(url_for("lancamentos.edit", id=id))

        try:
            conta_id = int(conta_id_str)
            valor = float(valor_str)

            if valor <= 0:
                raise ValueError

        except ValueError:
            flash("Valor deve ser um número positivo.", "error")
            return redirect(url_for("lancamentos.edit", id=id))

        try:
            datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            flash("Data inválida. Use formato YYYY-MM-DD.", "error")
            return redirect(url_for("lancamentos.edit", id=id))

        if tipo not in ["Débito", "Crédito"]:
            flash("Tipo deve ser Débito ou Crédito.", "error")
            return redirect(url_for("lancamentos.edit", id=id))

        try:

            lancamento.data = data
            lancamento.conta_id = conta_id
            lancamento.descricao = descricao
            lancamento.tipo = tipo
            lancamento.valor = valor

            lancamento.update()

            flash("Lançamento atualizado com sucesso.", "success")

        except Exception as e:

            print("Erro ao atualizar lançamento:", e)
            flash("Erro ao atualizar lançamento.", "error")

        return redirect(url_for("lancamentos.index"))

    contas = Conta.get_all()

    return render_template(
        "edit_lancamento.html",
        lancamento=lancamento,
        contas=contas
    )


# ===============================
# EXCLUIR LANÇAMENTO
# ===============================
@lancamentos_bp.route("/delete/<int:id>")
def delete(id):

    try:

        Lancamento.delete(id)

        flash("Lançamento excluído com sucesso.", "success")

    except Exception as e:

        print("Erro ao excluir lançamento:", e)
        flash("Erro ao excluir lançamento.", "error")

    return redirect(url_for("lancamentos.index"))