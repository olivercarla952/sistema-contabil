from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

from database.db import init_db

from routes.dashboard_routes import dashboard_bp
from routes.lancamentos_routes import lancamentos_bp
from routes.relatorios_routes import relatorios_bp

import os


# =========================================
# CRIAÇÃO DA APLICAÇÃO
# =========================================
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)


# =========================================
# CONFIGURAÇÕES
# =========================================
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")


# =========================================
# PROTEÇÃO CSRF
# =========================================
csrf = CSRFProtect(app)


# =========================================
# INICIALIZAR BANCO
# =========================================
with app.app_context():
    init_db()


# =========================================
# REGISTRO DAS ROTAS (BLUEPRINTS)
# =========================================
app.register_blueprint(dashboard_bp)
app.register_blueprint(lancamentos_bp)
app.register_blueprint(relatorios_bp)


# =========================================
# TRATAMENTO DE ERROS
# =========================================
@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template("erro.html", mensagem="Página não encontrada"), 404


@app.errorhandler(500)
def erro_interno(e):
    return render_template("erro.html", mensagem="Erro interno do servidor"), 500


# =========================================
# EXECUÇÃO DA APLICAÇÃO
# =========================================
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )