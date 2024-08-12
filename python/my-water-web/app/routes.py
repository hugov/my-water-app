import logging

from flask import current_app as app, render_template, flash, request, redirect
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

    products = ProductService.list_product()
    products_list = [product.to_dict() for product in products]

    return render_template('/product/index.html', products =  products_list, current_page = "products")

@app.route('/produto-adicionar', methods=['GET' , 'POST'])
def produto_adicionar():
    logger.info("Adicionando um novo produto")

    _product = Product()

    if request.method == 'GET':
        return render_template('/product/add.html', product = _product, current_page = "products")
    else:
        _product.name = request.form.get('name')
        _product.description = request.form.get('description')
        _product.price = request.form.get('price')
        _product.status = request.form.get('status')

        msg = validate_produto_adicionar(_product)
        if msg:
            flash(msg)
            return render_template('/product/add.html', product = _product, current_page = "products")

        ProductService.create_product(_product)
        return redirect('/produto-lista')

@app.route('/produto-consultar/<int:id>')
def produto_consultar(id):
    logger.info(f"Consultando o produto {id}")
    
    _product = ProductService.get_product(id)
    return render_template('/product/retrieve.html', product = _product, current_page = "products")

@app.route('/produto-alterar/<int:id>', methods=['GET', 'POST'])
def produto_alterar(id):
    logger.info("Acessou a listagem de produtos")

    _product = ProductService.get_product(id)

    if request.method == 'GET':
        return render_template('/product/update.html', product = _product, current_page = "products")
    else:
        _product.name = request.form.get('name')
        _product.description = request.form.get('description')
        _product.price = request.form.get('price')
        _product.status = request.form.get('status')

        msg = validate_produto_adicionar(_product)
        if msg:
            flash(msg)
            return render_template('/product/update.html', product = _product, current_page = "products")

        ProductService.create_product(_product)
        return redirect('/produto-lista')

@app.route('/produto-excluir/<int:id>')
def produto_exluir(id):
    logger.info("Acessou a listagem de produtos")
    ProductService.delete_product(id=id)
    return redirect('/produto-lista')

def validate_produto_adicionar(produto: Product):
    if not produto:
        return 'Nenhum produto foi informado'
    elif produto.description == None or produto.description == '':
        return 'Preencha a descrição do produto'
    elif len(produto.description) < 5 and len(produto.description) > 50:
        return 'A descrição do produto precisa ter entre 5 e 50 caracteres'
    else:
        return ''