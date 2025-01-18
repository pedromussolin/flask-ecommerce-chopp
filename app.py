import os
from flask import Flask
from config import Config
from database import db
from controllers.main_controller import main_bp
from controllers.user_controller import user_bp


# App
app = Flask(__name__, template_folder=os.path.join('views', 'templates'))
app.config.from_object(Config)


# Inicializa o banco de dados
db.init_app(app)

@app.before_request
def create_tables():
    db.create_all() 


# Registrar os Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(user_bp, url_prefix='/user')


# Inicialização da aplicação
if __name__ == '__main__':
    app.run(debug=True, port=5153)