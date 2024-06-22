from flask import Flask
from logging_config import setup_logging

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Configurar logging
    setup_logging()

    with app.app_context():

        # Importar e registrar blueprints
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)
        
        return app