import os
from flask import Flask, session, request, redirect, url_for
from database import db
from config import Config
from controllers.main_controller import main_bp
from controllers.user_controller import user_bp


# App
app = Flask(__name__, template_folder=os.path.join('views', 'templates'))
app.config.from_object(Config)


# Inicializa o banco de dados
db.init_app(app)


# Registrar os Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(user_bp, url_prefix='/user')


# Verificação de login antes de acessar qualquer rota
@app.before_request
def check_login():
    # Exclui rotas públicas da verificação
    public_routes = ['user.login', 'user.signup', 'static']  # Rotas públicas
    if 'user_id' not in session and request.endpoint not in public_routes:
        return redirect(url_for('user.login'))  # Redireciona para a página de login


# Inicialização da aplicação
if __name__ == '__main__':
    app.run(debug=True, port=5153)