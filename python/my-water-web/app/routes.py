import logging
import os

from flask import current_app as app, render_template, flash, request, redirect, request, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
from datetime import datetime

from app.services.product_service import ProductService
from app.services.category_service import CategoryService
from app.services.user_service import UserService
from app.services.profile_service import ProfileService
from app.models import Product, Category, User, Profile

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
    _categories = CategoryService.list_category()

    if request.method == 'GET':
        return render_template('/product/add.html', product = _product, categories = _categories, current_page = "products")
    else:
        _product.name = request.form.get('name')
        _product.description = request.form.get('description')
        _product.category_id = request.form.get('category_id')
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
    _categories = CategoryService.list_category()
    return render_template('/product/retrieve.html', product = _product, categories = _categories, current_page = "products")

@app.route('/produto-alterar/<int:id>', methods=['GET', 'POST'])
def produto_alterar(id):
    logger.info("Acessou a listagem de produtos")

    _product = ProductService.get_product(id)
    _categories = CategoryService.list_category()

    if request.method == 'GET':
        return render_template('/product/update.html', product = _product, categories = _categories, current_page = "products")
    else:
        _product.name = request.form.get('name')
        _product.description = request.form.get('description')
        _product.category_id = request.form.get('category_id')
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

def create_image_name():
    data = datetime.now()
    data_format = data.strftime("%Y%m%d%H%M%S")
    return f"categoria_{data_format}.jpg"

@app.route('/categoria-lista')
def categoria_lista():
    logger.info("Listando as categorias cadastradas")
    
    categories = CategoryService.list_category()
    categories_list = [category.to_dict() for category in categories]
    
    return render_template('/category/index.html', categories=categories_list, current_page="categories")

@app.route('/categoria-imagem/<filename>')
def get_categoria_imagem(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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

        if 'image' not in request.files:
            return redirect(request.url)
        
        file = request.files['image']
        
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            #filename = secure_filename(file.filename) # Nome vindo do HTML
            filename = secure_filename(create_image_name())
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Redimensionar e cortar a imagem
            #with Image.open(filepath) as img:
            #    img = img.resize((300, 300))  # Redimensionar para 300x300 pixels
            #    img.save(filepath)  # Salvar a imagem redimensionada
            
            # Salvar o caminho da imagem no banco de dados
            _category.image = filepath

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

        if 'image' in request.files and request.files['image'].filename != '':
            file = request.files['image']
            
            if file.filename == '':
                return redirect(request.url)
            
            if file:
                filename = secure_filename(_category.image.split('\\')[-1])
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                _category.image = filepath

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
    CategoryService.delete_category(id=id)
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
        _user.username = request.form.get('username')
        _user.password = request.form.get('password')
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
        _user.username = request.form.get('username')
        _user.password = request.form.get('password')
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
    UserService.delete_user(id=id)
    return redirect('/usuario-lista')


def validate_usuario_adicionar(user: Category):
    if not user:
        return 'Nenhum usuário foi informada'
    elif user.name is None or user.name == '':
        return 'Preencha o seu nome'
    else:
        return ''

#
# Rota: Perfil
#

@app.route('/perfil-lista')
def perfil_lista():
    logger.info("Listando as perfis cadastradas")
    
    profiles = ProfileService.list_profile()
    profiles_list = [profile.to_dict() for profile in profiles]
    
    return render_template('/profile/index.html', profiles=profiles_list, current_page="profiles")


@app.route('/perfil-adicionar', methods=['GET', 'POST'])
def perfil_adicionar():
    logger.info("Adicionando um perfis")
    
    _profile = Profile()
    
    if request.method == 'GET':
        return render_template('/profile/add.html', profile=_profile, current_page="profiles")
    else:
        _profile.name = request.form.get('name')
        _profile.description = request.form.get('description')
        _profile.allows_create = 1 if request.form.get('allows_create', 0) == 'on' else 0
        _profile.allows_retrieve = 1 if request.form.get('allows_retrieve', 0) == 'on' else 0
        _profile.allows_updated = 1 if request.form.get('allows_updated', 0) == 'on' else 0
        _profile.allows_delete = 1 if request.form.get('allows_delete', 0) == 'on' else 0
        _profile.status = request.form.get('status')
        
        msg = validate_perfil_adicionar(_profile)
        if msg:
            flash(msg)
            return render_template('/profile/add.html', profile=_profile, current_page="profiles")
        
        ProfileService.create_profile(_profile)
        return redirect('/perfil-lista')


@app.route('/perfil-consultar/<int:id>')
def perfil_consultar(id):
    logger.info(f"Consultando o perfis {id}")
    
    _profile = ProfileService.get_profile(id)
    return render_template('/profile/retrieve.html', profile=_profile, current_page="profiles")


@app.route('/perfil-alterar/<int:id>', methods=['GET', 'POST'])
def perfil_alterar(id):
    logger.info("Alterando a perfis")
    
    _profile = ProfileService.get_profile(id)
    
    if request.method == 'GET':
        return render_template('/profile/update.html', profile=_profile, current_page="profiles")
    else:
        _profile.name = request.form.get('name')
        _profile.description = request.form.get('description')
        _profile.allows_create = 1 if request.form.get('allows_create', 0) == 'on' else 0
        _profile.allows_retrieve = 1 if request.form.get('allows_retrieve', 0) == 'on' else 0
        _profile.allows_updated = 1 if request.form.get('allows_updated', 0) == 'on' else 0
        _profile.allows_delete = 1 if request.form.get('allows_delete', 0) == 'on' else 0
        _profile.status = request.form.get('status')
        
        msg = validate_perfil_adicionar(_profile)
        if msg:
            flash(msg)
            return render_template('/profile/update.html', profile=_profile, current_page="profiles")
        
        ProfileService.create_profile(_profile)
        return redirect('/perfil-lista')


@app.route('/perfil-excluir/<int:id>')
def perfil_excluir(id):
    logger.info(f"Excluindo o perfis {id}")
    ProfileService.delete_profile(id=id)
    return redirect('/perfil-lista')


def validate_perfil_adicionar(profile: Category):
    if not profile:
        return 'Nenhum perfil foi informada'
    elif profile.name is None or profile.name == '':
        return 'Preencha o nome do perfil'
    else:
        return ''

#
# Rota: Catalogo
#

@app.route('/catalogo-lista')
def catalogo_lista():
    logger.info("Listando as categorias cadastradas")
    
    #profiles = ProfileService.list_profile()
    #profiles_list = [profile.to_dict() for profile in profiles]
    #return render_template('/catalog/index.html', profiles=profiles_list, current_page="profiles")
    
    return render_template('/catalog/index.html', current_page="catalogs")