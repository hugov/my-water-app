import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    
    # Configura o logger raiz
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)

    # Formato dos logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Handler para o console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para o arquivo de log
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=25000, backupCount=5, delay=True, encoding='utf8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
