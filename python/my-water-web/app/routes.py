import logging

from flask import current_app as app, render_template, flash
from app.services.product_service import ProductService
from app.models import Product

logger = logging.getLogger(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/error404.html'), 404

@app.errorhandler(500)
def page_not_found(error):
    return render_template('error/error500.html'), 404

@app.route('/')
def home():
    logger.info("Acessou a página inicial")
    return render_template('home.html', current_page = "dashboard")

@app.route('/about')
def about():
    logger.info("Acessou a página sobre")
    return render_template('about.html')

# Rota de produtos
@app.route('/produto-lista')
def produto_lista():
    logger.info("Listando os produtos cadastrados")

    product_list = ProductService.list_product()
    return render_template('/product/index.html', products =  product_list, current_page = "products")

@app.route('/produto-adicionar')
def produto_adicionar():
    logger.info("Acessou a listagem de produtos")

    _product = Product()
    _product.name = 'Galão de água - Lindoia 20L'
    _product.name = 'G'
    _product.description = 'Galão de água - Lindoia 20L'
    _product.price = 15.0
    _product.status = 1

    msg = validate_produto_adicionar(_product)
    if msg:
        flash(msg)
        return render_template('/product/add.html', product = _product)

    product = ProductService.create_product(_product)

    return render_template('/product/add.html', product = product, current_page = "products")

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

def validate_produto_adicionar(produto: Product):
    if not produto:
        return 'Nenhum produto foi informado'
    elif produto.description == None or produto.description == '':
        return 'Preencha a descrição do produto'
    elif len(produto.description) >= 5 and len(produto.description) <= 50:
        return 'A descrição do produto precisa ter entre 5 e 50 caracteres'