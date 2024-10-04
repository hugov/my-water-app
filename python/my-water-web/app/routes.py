import logging
import os

from flask import current_app as app, url_for, render_template, flash, request, redirect, send_from_directory, session, jsonify, send_file, Response, make_response
from werkzeug.utils import secure_filename
from PIL import Image
from datetime import datetime
from fpdf import FPDF
from io import BytesIO

from app.services.product_service import ProductService
from app.services.category_service import CategoryService
from app.services.user_service import UserService
from app.services.profile_service import ProfileService
from app.services.order_service import OrderService
from app.services.report_service import ReportService

from app.models import Product, Category, User, Profile, Order, OrderItems

logger = logging.getLogger(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/error404.html'), 404

@app.errorhandler(500)
def page_not_found(error):
    return render_template('error/error500.html'), 404

@app.before_request
def check_login():
    allowed_routes = ['static', 'home', 'login', 'logout', 'catalogo_lista', 
        'get_categoria_imagem', 'catalogo_item', 'get_cart', 'add_to_cart', 
        'limpar_carrinho', 'mostrar_carrinho', 'finalizar_carrinho']

    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    logger.info("Acessou a página login")
    if request.method == "GET":
        return render_template('/admin/login.html')

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        date = datetime.now()
        date_format = date.strftime("%d%m%Y")
        password_today = f"admin#{date_format}"

        if username == "admin" and password == password_today:

            if 'user' not in session:
                session['user'] = "Admin"
                session['admin'] = True

            return redirect(url_for('catalogo_lista'))
        else:
            flash("Usuário ou senha estão incorretos.")

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('admin', None)
    session.pop('cart', None)

    return redirect(url_for('login'))

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
    allows_images_store_database = eval(os.environ.get('ALLOWS_IMAGES_STORE_DATABASE'))
    if allows_images_store_database:
        image = CategoryService.get_image_name(filename)
        return Response(image.image_data, mimetype='image/jpeg')
    else:
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
            filename = secure_filename(create_image_name())

            allows_images_store_database = eval(os.environ.get('ALLOWS_IMAGES_STORE_DATABASE'))
            if allows_images_store_database:
                _image_data = file.read()
                _category.image_data = _image_data
                _category.image = filename
            else:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                _category.image = filepath

        _category.status = request.form.get('status')
        
        msg = validate_form_category(_category)
        if msg:
            return jsonify({'errors': msg}), 400

        CategoryService.create_category(_category)
        return jsonify({'success': True}), 200

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
                
                allows_images_store_database = eval(os.environ.get('ALLOWS_IMAGES_STORE_DATABASE'))
                if allows_images_store_database:
                    _image_data = file.read()
                    _category.image_data = _image_data
                    _category.image = filename
                else:
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    _category.image = filepath
                

        _category.status = request.form.get('status')

        msg = validate_form_category(_category)
        if msg:
            return jsonify({'errors': msg}), 400
        
        CategoryService.create_category(_category)
        return jsonify({'success': True}), 200

@app.route('/categoria-excluir/<int:id>')
def categoria_excluir(id):
    logger.info(f"Excluindo a categoria {id}")
    CategoryService.delete_category(id=id)
    return redirect('/categoria-lista')

def validate_form_category(categoria: Category):
    errors = []

    # Validação do nome
    if not categoria.name:
        errors.append('O nome da categoria é obrigatório.')
    elif len(categoria.name) < 4 or len(categoria.name) > 50:
        errors.append('O nome da categoria deve ter entre 4 e 50 caracteres.')

    # Validação da descrição
    if not categoria.description:
        errors.append('A descrição da categoria é obrigatória.')
    elif len(categoria.description) < 4 or len(categoria.description) > 50:
        errors.append('A descrição da categoria deve ter entre 4 e 50 caracteres.')

    return errors

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
        _product.category_id = int(request.form.get('category_id'))
        _product.price = request.form.get('price')
        _product.status = request.form.get('status')

        msg = validate_form_product(_product)
        if msg:
            for error in msg:
                flash(error)
            return render_template('/product/add.html', product=_product, categories=_categories, current_page="products")

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
        _product.category_id = int(request.form.get('category_id'))
        _product.price = request.form.get('price')
        _product.status = request.form.get('status')

        msg = validate_form_product(_product)
        if msg:
            for error in msg:
                flash(error)
            return render_template('/product/update.html', product=_product, categories=_categories, current_page="products")

        ProductService.create_product(_product)
        return redirect('/produto-lista')

@app.route('/produto-excluir/<int:id>')
def produto_exluir(id):
    logger.info("Acessou a listagem de produtos")
    ProductService.delete_product(id=id)
    return redirect('/produto-lista')

def validate_form_product(produto: Product):
    errors = []

    # Validação do nome
    if not produto.name:
        errors.append('O nome do produto é obrigatório.')
    elif len(produto.name) < 4 or len(produto.name) > 50:
        errors.append('O nome do produto deve ter entre 4 e 50 caracteres.')

    # Validação da descrição
    if not produto.description:
        errors.append('A descrição do produto é obrigatória.')
    elif len(produto.description) < 4 or len(produto.description) > 50:
        errors.append('A descrição do produto deve ter entre 4 e 50 caracteres.')

    # Validação da categoria
    if not produto.category_id:
        errors.append('A categoria do produto é obrigatória.')

    # Validação do preço
    if not produto.price:
        errors.append('O preço do produto é obrigatório.')
    else:
        try:
            if float(produto.price) <= 0.00:
                errors.append('O preço do produto deve ser maior que R$ 0,00.')
        except ValueError:
            errors.append('O preço do produto deve ser um número válido.')

    return errors

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

@app.route('/')
@app.route('/catalogo-lista')
def catalogo_lista():
    logger.info("Listando as categorias cadastradas")

    _categories = CategoryService.list_category()
    return render_template('/catalog/index.html', categories = _categories, current_page="catalogs")


@app.route('/catalogo/<int:category_id>')
def catalogo_item(category_id: int):
    logger.info("Listando as categorias cadastradas")

    _products = ProductService.list_product_by_category(category_id)
    return render_template('/catalog/item.html', products = _products, current_page="catalogs")

#
# Rota: Carrinho de compras
#

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.json['id']
    product_name = request.json['name']
    product_price = request.json['price']
    quantity = request.json['quantity']
    
    if 'cart' not in session:
        session['cart'] = []
    
    # Adiciona ou atualiza o item no carrinho
    cart = session['cart']
    existing_item = next((item for item in cart if item['name'] == product_name), None)
    if existing_item:
        existing_item['quantity'] += quantity
    else:
        cart.append({'id': product_id, 'name': product_name, 'price': product_price, 'quantity': quantity})

    session.modified = True  # Marca a sessão como modificada
    return jsonify(cart)

@app.route('/get_cart', methods=['GET'])
def get_cart():
    return jsonify(session.get('cart', []))

@app.route('/limpar_carrinho', methods=['GET'])
def limpar_carrinho():
    session.pop('cart', None)
    return redirect('/catalogo-lista')

@app.route('/mostrar-carrinho', methods=['GET'])
def mostrar_carrinho():
    return render_template('/catalog/cart.html')

@app.route('/finalizar-carrinho', methods=['POST'])
def finalizar_carrinho():
    logger.info('Finalizando o carrinho de compra')

    order = Order()
    order.name = request.form.get('name')
    order.train_carriage = int(request.form.get('train_carriage', 0))
    order.seat = int(request.form.get('seat', 0))
    order.status = 1

    OrderService.create_order(order)
    logger.debug(f"Pedido {order} inserido com sucesso")

    total_order_value = 0

    cart = session.get('cart')
    if cart:
        for item_tmp in cart:
           order_item = OrderItems()
           order_item.order_id = order.id
           order_item.product_id = item_tmp.get('id')
           
           quantity = item_tmp.get('quantity')
           order_item.quantity = quantity

           total_value = float(item_tmp.get('price', 0)) * quantity
           order_item.total_value = total_value

           total_order_value = round(total_order_value + total_value, 2)

           OrderService.create_order_item(order_item)
           logger.debug(f"Itens do pedido {order_item} inserido com sucesso")

    order.total_value = total_order_value
    OrderService.create_order(order)

    session.pop('cart', None)
    logger.debug("Itens removidos da sessão")

    return render_template('/catalog/index.html')

#
# Rota: Relatórios
#

@app.route('/relatorio-vendas', methods=['GET', 'POST'])
def relatorio_vendas():
    logger.info("Exibindo o relatório de vendas")
    
    if request.method == 'GET':
        return render_template('report/report_sales.html', current_page="report_sales")
    else:

        start_date = request.form.get('data_inicio')
        end_date = request.form.get('data_fim')

        vendas = ReportService.report_sales(start_date, end_date)

        if request.method == 'POST' and request.form.get('export_pdf'):
            return exportar_pdf(vendas)

        return render_template('report/report_sales.html', vendas=vendas, current_page="report_sales")

class Venda:
    def __init__(self, categoria, produto, quantidade, data_venda):
        self.categoria = categoria
        self.produto = produto
        self.quantidade = quantidade
        self.data_venda = data_venda

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Relatório de Vendas", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

def exportar_pdf(vendas):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Cabeçalho da tabela
    pdf.set_fill_color(240, 240, 240)  # Cor de fundo para o cabeçalho
    pdf.cell(50, 10, 'Categoria', border=1, fill=True)
    pdf.cell(50, 10, 'Produto', border=1, fill=True)
    pdf.cell(30, 10, 'Quantidade', border=1, fill=True)
    pdf.cell(50, 10, 'Data de Venda', border=1, fill=True)
    pdf.ln()

    # Corpo da tabela
    pdf.set_fill_color(255, 255, 255)  # Cor de fundo para as linhas do corpo
    for venda in vendas:
        pdf.cell(50, 10, venda.categoria, border=1, fill=True)
        pdf.cell(50, 10, venda.produto, border=1, fill=True)
        pdf.cell(30, 10, str(venda.quantidade), border=1, fill=True)
        pdf.cell(50, 10, venda.data_venda.strftime("%d/%m/%Y"), border=1, fill=True)
        pdf.ln()

    buffer = BytesIO()
    pdf_output = pdf.output(dest='S')  # Gera o PDF como uma string
    buffer.write(pdf_output.encode('latin1'))  # Escreve no buffer como bytes
    buffer.seek(0)  # Reposiciona o ponteiro no início do buffer

    response = make_response(buffer.getvalue())  # Cria a resposta Flask com o conteúdo do buffer
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=relatorio_vendas.pdf'
    
    #return response
    return send_file(buffer, as_attachment=True, download_name='relatorio_vendas.pdf', mimetype='application/pdf')