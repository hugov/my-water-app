from flask import Flask
from logging_config import setup_logging
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# Inicializar a extensão SQLAlchemy
db = SQLAlchemy()

def create_app():
    
    # Carregar variáveis de ambiente do .env
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Inicializar o banco de dados
    db.init_app(app)

    # Configurar logging
    setup_logging()

    with app.app_context():
        
        # Adicionando as rotas no projeto
        from . import routes

        # Criar as tabelas no banco de dados, senão existirem
        db.create_all()

    return app