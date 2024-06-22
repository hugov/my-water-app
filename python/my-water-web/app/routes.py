from flask import Blueprint, render_template
import logging

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main.route('/')
def home():
    logger.info("Acessou a página inicial")
    return render_template('home.html')

@main.route('/about')
def about():
    logger.info("Acessou a página sobre")
    return render_template('about.html')