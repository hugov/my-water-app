import logging

from flask import current_app as app, render_template, jsonify
from app.services.product_service import ProductService
from app.models import Product

logger = logging.getLogger(__name__)

@app.route('/')
def home():
    logger.info("Acessou a página inicial")
    return render_template('home.html')

@app.route('/about')
def about():
    logger.info("Acessou a página sobre")
    return render_template('about.html')

# Rota de produtos
@app.route('/produto-lista')
def produto_lista():
    logger.info("Listando os produtos cadastrados")
    return render_template('/product/index.html')

@app.route('/produto-adicionar')
def produto_adicionar():
    logger.info("Acessou a listagem de produtos")

    _product = Product()
    _product.name = 'Galão de água - Lindoia 20L'
    _product.description = 'Galão de água - Lindoia 20L'
    _product.price = 15.0
    _product.status = 1

    product = ProductService.create_product(_product)
    #return jsonify(product)

    return render_template('/product/add.html', product = product)

@app.route('/produto-consultar')
def produto_consultar():
    logger.info("Acessou a listagem de produtos")
    return render_template('/product/retrieve.html')

@app.route('/produto-alterar')
def produto_alterar():
    logger.info("Acessou a listagem de produtos")
    return render_template('/product/update.html')

@app.route('/produto-excluir')
def produto_exluir():
    logger.info("Acessou a listagem de produtos")
    return render_template('/product/index.html')