import logging

from flask import current_app as app, render_template, flash, request, redirect
from app.services.product_service import ProductService
from app.services.category_service import CategoryService
from app.services.user_service import UserService
from app.models import Product, Category, User

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

#
# Rota: Produto
#

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

#
# Rota: Categoria
#

@app.route('/categoria-lista')
def categoria_lista():
    logger.info("Listando as categorias cadastradas")
    
    categories = CategoryService.list_category()
    categories_list = [category.to_dict() for category in categories]
    
    return render_template('/category/index.html', categories=categories_list, current_page="categories")


@app.route('/categoria-adicionar', methods=['GET', 'POST'])
def categoria_adicionar():
    logger.info("Adicionando uma nova categoria")
    
    _category = Category()
    
    if request.method == 'GET':
        return render_template('/category/add.html', category=_category, current_page="categories")
    else:
        _category.name = request.form.get('name')
        _category.description = request.form.get('description')
        _category.image = request.form.get('image')
        _category.creation_date = request.form.get('creation_date')
        _category.status = request.form.get('status')
        
        msg = validate_categoria_adicionar(_category)
        if msg:
            flash(msg)
            return render_template('/category/add.html', category=_category, current_page="categories")
        
        CategoryService.create_category(_category)
        return redirect('/categoria-lista')


@app.route('/categoria-consultar/<int:id>')
def categoria_consultar(id):
    logger.info(f"Consultando a categoria {id}")
    
    _category = CategoryService.get_category(id)
    return render_template('/category/retrieve.html', category=_category, current_page="categories")


@app.route('/categoria-alterar/<int:id>', methods=['GET', 'POST'])
def categoria_alterar(id):
    logger.info("Alterando a categoria")
    
    _category = CategoryService.get_category(id)
    
    if request.method == 'GET':
        return render_template('/category/update.html', category=_category, current_page="categories")
    else:
        _category.name = request.form.get('name')
        _category.description = request.form.get('description')
        _category.image = request.form.get('image')
        _category.creation_date = request.form.get('creation_date')
        _category.status = request.form.get('status')
        
        msg = validate_categoria_adicionar(_category)
        if msg:
            flash(msg)
            return render_template('/category/update.html', category=_category, current_page="categories")
        
        CategoryService.create_category(_category)
        return redirect('/categoria-lista')


@app.route('/categoria-excluir/<int:id>')
def categoria_excluir(id):
    logger.info(f"Excluindo a categoria {id}")
    CategoryService.delete_categoria(id=id)
    return redirect('/categoria-lista')


def validate_categoria_adicionar(categoria: Category):
    if not categoria:
        return 'Nenhuma categoria foi informada'
    elif categoria.name is None or categoria.name == '':
        return 'Preencha o nome da categoria'
    elif categoria.description is None or categoria.description == '':
        return 'Preencha a descrição da categoria'
    elif len(categoria.description) < 5 or len(categoria.description) > 50:
        return 'A descrição da categoria precisa ter entre 5 e 50 caracteres'
    else:
        return ''


#
# Rota: Usuário
#

@app.route('/usuario-lista')
def usuario_lista():
    logger.info("Listando as usuários cadastradas")
    
    users = UserService.list_user()
    users_list = [user.to_dict() for user in users]
    
    return render_template('/user/index.html', users=users_list, current_page="users")


@app.route('/usuario-adicionar', methods=['GET', 'POST'])
def usuario_adicionar():
    logger.info("Adicionando um usuário")
    
    _user = User()
    
    if request.method == 'GET':
        return render_template('/user/add.html', user=_user, current_page="users")
    else:
        _user.name = request.form.get('name')
        _user.email = request.form.get('email')
        _user.document = request.form.get('document')
        _user.phone = request.form.get('phone')
        _user.username = request.form.get('phone')
        _user.password = request.form.get('phone')
        _user.creation_date = request.form.get('creation_date')
        _user.status = request.form.get('status')
        
        msg = validate_usuario_adicionar(_user)
        if msg:
            flash(msg)
            return render_template('/user/add.html', user=_user, current_page="users")
        
        UserService.create_user(_user)
        return redirect('/usuario-lista')


@app.route('/usuario-consultar/<int:id>')
def usuario_consultar(id):
    logger.info(f"Consultando o usuário {id}")
    
    _user = UserService.get_user(id)
    return render_template('/user/retrieve.html', user=_user, current_page="users")


@app.route('/usuario-alterar/<int:id>', methods=['GET', 'POST'])
def usuario_alterar(id):
    logger.info("Alterando a usuário")
    
    _user = UserService.get_user(id)
    
    if request.method == 'GET':
        return render_template('/user/update.html', user=_user, current_page="users")
    else:
        _user.name = request.form.get('name')
        _user.email = request.form.get('email')
        _user.document = request.form.get('document')
        _user.phone = request.form.get('phone')
        _user.username = request.form.get('phone')
        _user.password = request.form.get('phone')
        _user.creation_date = request.form.get('creation_date')
        _user.status = request.form.get('status')
        
        msg = validate_usuario_adicionar(_user)
        if msg:
            flash(msg)
            return render_template('/user/update.html', user=_user, current_page="users")
        
        UserService.create_user(_user)
        return redirect('/usuario-lista')


@app.route('/usuario-excluir/<int:id>')
def usuario_excluir(id):
    logger.info(f"Excluindo o usuário {id}")
    UserService.delete_categoria(id=id)
    return redirect('/usuario-lista')


def validate_usuario_adicionar(user: Category):
    if not user:
        return 'Nenhum usuário foi informada'
    elif user.name is None or user.name == '':
        return 'Preencha o seu nome'
    else:
        return ''
