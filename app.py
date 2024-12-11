from http.cookies import SimpleCookie
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
from urllib.parse import parse_qs,urlparse
import os
import csv   
import cgi

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from admin_controller.adimin_user_controller import AdminLoginController
from admin_controller.admin_category_controller import CetegoryController
from admin_controller.admin_product_controller import ProductController
from admin_controller.dashboard_controller import DashboardController
from admin_controller.order_admin_controller import OrderController
from admin_controller.slide_controller import Controller_slide
from admin_model.order import OrderModel



class RequestHandler(SimpleHTTPRequestHandler):

    #admin_controller = AdminLoginController()
    #response = admin_controller.create_superadmin('superadmin_user', '1234')
    #print(response)
    def ajax(self):
      
        return self.headers.get('X-Requested-With') == 'XMLHttpRequest'
      
    def get_user_id_from_cookies(self):
        # Obtém os cookies do cabeçalho
        
        cookie_header = self.headers.get('Cookie')
        
        if cookie_header:
            # Parseia os cookies
            cookie = SimpleCookie(cookie_header)
            
            # Verifica se o cookie 'user_id' existe
            if 'user_id' in cookie:
                return cookie['user_id'].value
        return None 
    def check_user_login_status(self):
        # Verifica se o usuário está logado baseado no cookie 'user_id'
        user_id = self.get_user_id_from_cookies()
       
        return user_id is not None
    def get_query_param(self, param_name):
        """Extrai o valor de um parâmetro da query string da URL"""
        from urllib.parse import urlparse, parse_qs
        # Parseia a URL completa
        query_components = parse_qs(urlparse(self.path).query)
        # Retorna o valor do parâmetro, se existir
        return query_components.get(param_name, [None])[0]
    def __init__(self, *args, **kwargs):
        self.logged_in_user = None  # Inicializa o atributo logged_in_user
        super().__init__(*args, directory='admin_views', **kwargs)  # Certifique-se de que o super() seja chamado depois
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()


    def do_GET(self):
     if self.path.startswith('/css/') or self.path.startswith('/js/'):
      return super().do_GET()
       
        # Manipula as rotas GET
     parsed_path = urlparse(self.path)
     path = parsed_path.path
     query_params = parse_qs(parsed_path.query)
   
     if self.path == '/admin':
        user_is_logged_in = self.check_user_login_status()
        if user_is_logged_in == True:
         
            self.handle_dashboard()
        else:
            self.handle_login_page()

     elif self.path == '/login':
            self.handle_login_page()
    
     elif self.path == '/users_page':
            ajax = self.ajax()
            user_is_logged_in = self.check_user_login_status()
            if ajax == True:
             print(ajax)
             if user_is_logged_in == True:
              self.users_page()
             else:
              self.handle_login_page()
            else:
              self.handle_dashboard()
     elif self.path == '/add_users':
            ajax = self.ajax()
            user_is_logged_in = self.check_user_login_status()
            if ajax == True:
             print(ajax)
             if user_is_logged_in == True:
              self.add_users()
             else:
              self.handle_login_page()
            else:
                 self.handle_dashboard()


     elif path == '/edit_users':
              ajax = self.ajax()
              user_is_logged_in = self.check_user_login_status()
              if ajax == True:
               if user_is_logged_in == True:
                id = query_params.get('id', [None])[0]
                if id:
                 self.handle_admin_users_edit_page(id)
                else:
                 self.handle_login_page()
              else:
                 self.handle_dashboard()

     elif self.path.startswith("/download_csv"):
               user_is_logged_in = self.check_user_login_status()
               if user_is_logged_in == True:
                query_components = parse_qs(urlparse(self.path).query)
                order_status = query_components.get("status", [None])[0]
                if order_status:
                  self.handle_download_order_report_csv(order_status)
                else:
                 self.send_response(400)
                 self.end_headers()
               else:
                 self.handle_login_page()
     if self.path.startswith("/download_excel"):
            user_is_logged_in = self.check_user_login_status()
            if user_is_logged_in == True:
             query_components = parse_qs(urlparse(self.path).query)
             order_status = query_components.get("status", [None])[0]

             if order_status:
                self.handle_download_order_report_excel(order_status)
             else:
                self.send_response(400)
                self.end_headers()
            else:
                 self.handle_login_page()
       
     elif self.path == '/logout':
            self.handle_logout()

     elif self.path == '/display_products':
            ajax = self.ajax()
            user_is_logged_in = self.check_user_login_status()
            if ajax == True:
             if user_is_logged_in == True:
              self.handle_admin_products_page()
             else:
                 self.handle_login_page()
            else:
                 self.handle_dashboard()

     elif self.path == '/add_products':
            ajax = self.ajax()
            user_is_logged_in = self.check_user_login_status()
            if ajax == True:
             if user_is_logged_in == True:
              self.handle_admin_product_add_page()
             else:
                 self.handle_login_page()
            else:
                 self.handle_dashboard()


     elif path == '/edit_products':
              ajax = self.ajax()
              user_is_logged_in = self.check_user_login_status()
              if ajax == True:
               if user_is_logged_in == True:
                product_id = query_params.get('id', [None])[0]
                if product_id:
                 self.handle_admin_product_edit_page(product_id)
                else:
                 self.handle_login_page()
              else:
                 self.handle_dashboard()

        

     elif self.path == '/lista_de_pedidos':
            ajax = self.ajax()
            user_is_logged_in = self.check_user_login_status()
            if ajax == True:
             if user_is_logged_in == True:
              self.handle_admin_orders_page()
             else:
              self.handle_login_page()
            else:
                 self.handle_dashboard()
         

     elif path == '/view_order':

               ajax = self.ajax()
               user_is_logged_in = self.check_user_login_status()
               if ajax == True:
                if user_is_logged_in == True:
                 order_id = query_params.get('order_id', [None])[0]
                 if order_id:
                  self.details_admin_orders_page(order_id)
                 else:
                  self.handle_login_page()
                else:
                 self.handle_dashboard()

     elif path == '/update_status':
              ajax = self.ajax()
              user_is_logged_in = self.check_user_login_status()
              if ajax == True:
               if user_is_logged_in == True:
                order_id = query_params.get('order_id', [None])[0]
               if order_id:
                self.update_status_orders_page(order_id)
               else:
                 self.handle_login_page()
              else:
                 self.handle_dashboard()

     elif self.path == '/report':
            ajax = self.ajax()
            user_is_logged_in = self.check_user_login_status()
            if ajax == True:
             if user_is_logged_in == True:
              self.report_page()
             else:
                 self.handle_login_page()
            else:
                 self.handle_dashboard()
     elif self.path.startswith('/uploads/'):
            # Remove the leading "/" from the path
             file_path = self.path[1:]  # Remove the first character "/"
             if os.path.isfile(file_path):
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')  # Ajuste para o tipo correto
                self.end_headers()
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
             else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Arquivo nao encontrado.")
           
     elif self.path == '/list_slide':
            ajax = self.ajax()
            user_is_logged_in = self.check_user_login_status()
            if ajax == True:
             if user_is_logged_in == True:
              self.handle_list_slide()
             else:
                self.handle_login_page()
            else:
                 self.handle_dashboard()

     elif self.path == '/add_slide':
            ajax = self.ajax()
            user_is_logged_in = self.check_user_login_status()
            if ajax == True:
             if user_is_logged_in == True:
              self.handle_admin_product_add_slide()
             else:
                self.handle_login_page()
            else:
                 self.handle_dashboard()
        
     elif path == '/update_slides':
              ajax = self.ajax()
              user_is_logged_in = self.check_user_login_status()
              if ajax == True:
               if user_is_logged_in == True:
                slide_id = query_params.get('slide_id', [None])[0]
              
                if slide_id:
                 self.handle_edit_slid(slide_id)
               else:
                 self.handle_login_page()
              else:
                 self.handle_dashboard()
        
     elif self.path == '/add_category':
            ajax = self.ajax()
            user_is_logged_in = self.check_user_login_status()
            if ajax == True:
             if user_is_logged_in == True:
              self.add_category_get()
             else:
                self.handle_login_page()
            else:
                 self.handle_dashboard()
     elif self.path == '/list_category':
            ajax = self.ajax()
            user_is_logged_in = self.check_user_login_status()
            if ajax == True:
             if user_is_logged_in == True:
              self.list_category_get()
             else:
                self.handle_login_page()
            else:
                 self.handle_dashboard()
     elif path == '/update_categorys':
              ajax = self.ajax()
              user_is_logged_in = self.check_user_login_status()
              if ajax == True:
               if user_is_logged_in == True:
                cat_id = query_params.get('cat_id', [None])[0]
              
                if cat_id:
                 self.handle_admin_category_edit_page(cat_id)
               else:
                 self.handle_login_page()
              else:
                 self.handle_dashboard()
     elif self.path == '/api/sales_data':
            sales_data = OrderModel.generate_order_report_payments()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(sales_data).encode())
           
  

    def do_POST(self):
        # Manipula as rotas POST
        if self.path == '/login':
            self.handle_login()

        elif self.path == '/add_users_admin':
             self.add_users_admin()

        elif self.path == '/add_product_post':
             self.handle_admin_product_add()
        elif self.path == "/edit":
             product_id = None
             self.handle_admin_product_edit(product_id)
             
        elif self.path == '/edit_users_post':
             id = None
             self.handle_admin_users_edit_post(id)

        elif self.path == '/edit_slid_post':
             slide_id  = None
             self.handle_admin_slide_edite(slide_id )

        elif self.path == '/update_status_order':
             order_id = None
             self.status_update(order_id)

        elif self.path == "/delete_users":
             id = None
             self.delet_users(id)
            
        elif self.path == "/delete":
             product_id = None
             self.handle_admin_product_delete(product_id)

        elif self.path == "/delete_slide":
             slide_id  = None
             self.delet_slides(slide_id)

        elif self.path == "/delete_cat":
             cat_id  = None
             self.delet_category(cat_id)

        elif self.path == "/update_cat":
             cat_id  = None
             self.handle_update_category(cat_id)

        elif self.path == "/generate_report":
            
             self.generate_report_post()
        elif self.path == '/add_slide_post':
             self.handle_admin_slide_add()    
        elif self.path == '/add_category_post':
             self.add_category_post()    
        else:
            self.handle_404()

   







    #Login admin
    def handle_login_page(self):
    # Exibe o formulário de login
     self.send_response(200)
     self.send_header('Content-type', 'text/html')
     self.end_headers()

     content = f"""
            <html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login-Admin</title>
    <link rel="stylesheet" href="css/login.css">
</head>
<body>
          
            <form action="/login" method="POST">
                <label for="username">Usuário:</label>
                <input type="text" id="username" name="username" required><br><br>

                <label for="password">Senha:</label>
                <input type="password" id="password" name="password" required><br><br>

                <button type="submit">Login</button>
            </form>
        </body>
    </html>
    """
     self.wfile.write(content.encode('utf-8'))




    #post login admin
    def handle_login(self):
    # Obtém o tamanho dos dados enviados pelo formulário
     content_length = int(self.headers['Content-Length'])
     post_data = self.rfile.read(content_length).decode('utf-8')
     form_data = parse_qs(post_data)

    # Cria um pedido com os dados
     request = {
        'method': 'POST',
        'path': '/login',
        'get': lambda key: form_data.get(key, [None])[0],
        'session': {}  # Exemplo simples, você deve ter uma sessão real
     }

     login_controller = AdminLoginController()
     response = login_controller.login(request)

     if response["status"] == "success":
        # Armazene o ID do usuário na sessão
        request['session']['user_id'] = response['user_id']
        self.send_response(302)
        self.send_header('Location', '/admin')
        self.send_header('Set-Cookie', f'user_id={response["user_id"]}; Path=/; HttpOnly')
        self.end_headers()
     else:
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        error_message = response["message"]

            # HTML da página de login com mensagem de erro
        content = f"""
            <html>
                <head>
                    <title>Login - Administrador</title>
                </head>
                <body>
                    <h1>Login - Administrador</h1>
                    <form action="/login" method="POST">
                        <label for="username">Usuário:</label>
                        <input type="text" id="username" name="username" required><br><br>

                        <label for="password">Senha:</label>
                        <input type="password" id="password" name="password" required><br><br>

                        <button type="submit">Login</button>
                    </form>
                    {f'<p style="color: red;">{error_message}</p>' if error_message else ''}
                </body>
            </html>
            """
        self.wfile.write(content.encode('utf-8'))


    def handle_logout(self):
    # Limpa o estado de login
     self.logged_in_user = None  
     self.send_response(302)
     self.send_header('Location', '/login')  # Redireciona para a página de login
     self.send_header('Set-Cookie', 'user_id=; Expires=Thu, 01 Jan 1970 00:00:00 GMT;')  # Remove o cookie
     self.end_headers()       
             
    #pagina admin

    def handle_dashboard(self):
     try:
        # Controlador para obter os dados do dashboard
        admin_controller = DashboardController()
        dashboard_data = admin_controller.get_dashboard_data()
       
        user_id = self.get_user_id_from_cookies()
        userss = AdminLoginController.get_users_by_id(self,user_id)
        sales_data = OrderModel.generate_order_report_payments()
        role = userss["role"]
        if role == "superadmin" or role == "store_admin":
            superAdmins = AdminLoginController()
            superAdmin =superAdmins.get_users_super_by_id(role,user_id)
            for s in superAdmin:
             super = s["role"]
            
             if super == "store_admin":
              print(super)
              store_user_html = f"""
               <li><a class="nav-link" data-url="/display_products" href="#">Gerenciar Produtos</a></li>
                <li><a class="nav-link" data-url="/report"  href="#">Gerar Relatórios</a></li>
                 <li><a class="nav-link" data-url="/list_category" href="#">Gerenciar Categorias</a></li>
                 
                <li><a class="nav-link" data-url="/list_slide"  href="#">Slides Promocionais</a></li>
                 """
             elif super == "superadmin":
              store_user_html = f"""
             
              <li><a class="nav-link" data-url="/display_products" href="#">Gerenciar Produtos</a></li>
             <li><a class="nav-link" data-url="/report"  href="#">Gerar Relatórios</a></li>
             <li><a class="nav-link" data-url="/list_category" href="#">Gerenciar Categorias</a></li>
             <li><a class="nav-link" data-url="/list_slide"  href="#">Slides Promocionais</a></li>
            <li><a class="nav-link" data-url="/users_page" href="#">Gerenciar Usuários</a></li> """
        else: 
           store_user_html =""
          
        users_name = ""f"""<span>
                Olá, {userss["username"]} ! Bem-vindo à sua conta.
            </span>"""
       
        
        # Renderizar as estatísticas do dashboard
        
        role = userss["role"]
        if role == "superadmin" or role == "store_admin":
            superAdmins = AdminLoginController()
            superAdmin =superAdmins.get_users_super_by_id(role,user_id)
            for s in superAdmin:
             super = s["role"]
            
             if super == "superadmin" or super == "store_admin" : 
              stats_html = "".join(
            f"""
             <div class="dashboard-card">
                <h3>Produtos</h3>
                <div class="value" id="total-products">{dashboard_data['total_products']}</div>
                <div class="percentage">+5% desde a última semana</div>
            </div>
            <div class="dashboard-card">
                <h3>Pedidos</h3>
                <div class="value" id="total-orders">{dashboard_data['total_orders']}</div>
                <div class="percentage negative">-3% desde a última semana</div>
            </div>
            <div class="dashboard-card">
                <h3>Clientes</h3>
                <div class="value" id="total-users">{dashboard_data['total_users']}</div>
                <div class="percentage">+2% desde a última semana</div>
            </div>
           <div class="dashboard-card">
                <h3>Visitas</h3>
                <div class="value" id="total-visitors">3,500</div>
                <div class="percentage">+10% desde a última semana</div>
            </div>
              </div>
    
        <!-- Gráfico e outras seções da dashboard -->
        <section>
            <h3>Relatórios de Vendas</h3>
            <canvas id="salesChart" width="400" height="200"></canvas>
          
        </section>
    
            """
                )
        
        else:
         stats_html=""
             
       
                  
        # Renderizar o conteúdo principal da página
        html_content = self._render_template(
            "dashboard",
            {
                
                "stats_html": stats_html,
                "user_html": users_name,
                "store": store_user_html,
                "sales_data": sales_data
            }
        )

        # Verifica se o conteúdo foi gerado com sucesso
        if html_content:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.handle_404()

     except Exception as e:
        self.send_response(500)
        self.end_headers()
        self.wfile.write(f"Erro ao carregar o painel de controle: {str(e)}".encode('utf-8'))



    #Adicionar usuários
    def add_users(self):
       
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      role_controller = AdminLoginController()
      roles = role_controller.list_users_admin()
      for role in roles:
      
       content = f"""
   
         
           <h1>Administrador/Atendente</h1>
<form action="/add_users_admin" method="POST" class="user-form">
    <label for="username">Nome do usuário</label>
    <input type="text" id="username" name="username" required><br><br>

    <label for="password">Senha:</label>
    <input type="password" id="password" name="password" required><br><br>

    <label for="role">Nível do usuário</label>
    <select id="role" name="role">
        <option value="superadmin" {'selected' if role == 'superadmin' else ''}>Super Admin</option>
        <option value="store_admin" {'selected' if role == 'store_admin' else ''}>Store Admin</option>
        <option value="support_admin" {'selected' if role == 'support_admin' else ''}>Support Admin</option>
    </select>

    <button type="submit">Salvar</button>
</form>

        
    """
      self.wfile.write(content.encode('utf-8'))


    #Editar usuarios
    def handle_admin_users_edit_page(self, id):
       users_admin_controller = AdminLoginController()
       users = users_admin_controller.get_users_by_id(id)
       
       
       content = f"""
  
            <h1>Editar Usuário</h1>
            <form action="/edit_users_post" method="POST" class="user-form">
                <input type="hidden" name="id" value="{users['id']}">
                 <label for="username">Preço:</label>
                <input type="text" id="price" name="username" value="{users['username']}" required><br><br>

                <label for="discount_price">Preço com Desconto:</label>
                <input type="password" id="password" name="password" value="{users['password']}"><br><br>

                <select id="role" name="role">
                <option value="superadmin">{users['role']}</option>
                <option value="superadmin" {'selected' if users == 'superadmin' else ''}>Super Admin</option>
                <option value="store_admin" {'selected' if users == 'store_admin' else ''}>Store Admin</option>
                <option value="support_admin" {'selected' if users == 'support_admin' else ''}>Support Admin</option>
                </select>
                 <button type="submit">Atualizar</button>
            </form>
        
    """
       self.send_response(200)
       self.send_header('Content-type', 'text/html')
       self.end_headers()
       self.wfile.write(content.encode('utf-8'))
  
   #Post Adicionar usuários

    def add_users_admin(self):

         content_length = int(self.headers['Content-Length'])
         post_data = self.rfile.read(content_length)
         data = parse_qs(post_data.decode('utf-8'))
        
         username  = data.get('username', [None])[0]
         password = data.get('password', [None])[0]
         role = data.get('role', [None])[0]
         controller = AdminLoginController()
         controller.create_superadmin(username, password, role)
         self.send_response(302)  # Redireciona
         self.send_header('Location', '/admin')  # Para uma página de sucesso
         self.end_headers()
   
   #Post editar usuarios
    def handle_admin_users_edit_post(self, id):
 
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode('utf-8'))
        # Pegue os parâmetros do corpo da requisição
        id = data.get('id', [None])[0]
        username  = data.get('username', [None])[0]
        password = data.get('password', [None])[0]
        role = data.get('role', [None])[0]

        # Aqui você chamaria a função de atualização, como update_user
        users = AdminLoginController()
        users.update_users(id, username, password, role)

        
        self.send_response(302)  # Redireciona
        self.send_header('Location', '/users_page')  # Para uma página de sucesso
        self.end_headers()


     #deletar usuarios
   
   
    #Post deletar usuario
    def delet_users(self,id):
       content_length = int(self.headers['Content-Length'])
       post_data = self.rfile.read(content_length)
       data = parse_qs(post_data.decode('utf-8'))
       id = data.get('id', [None])[0]
       delet_user = AdminLoginController()
       delet_user.delete_user(id)
       self.send_response(302)  # Redireciona
       self.send_header('Location', '/users_page')  # Para uma página de sucesso
       self.end_headers()


    #Exibir a lista de usuários
    def users_page(self):
         self.send_response(200)
         self.send_header('Content-type', 'text/html')
         self.end_headers()

         users_admin_controller = AdminLoginController()
         users = users_admin_controller.list_users_admin()
        
         
         content = """
                <h1>Lista de Usuários</h1>
          
            <a  class="nav-link" data-url="/add_users"  href="#"><i class="fa fa-plus" aria-hidden="true"></i></a> 
            <table border="1">
                <tr>
                    <th>ID</th>
                    <th>Nome</th>
                    <th>Nivel</th>
                    <th>Ações</th>
                </tr>
    """
         for user in users:
      
          content += f"""
                <tr>
                    <td>{user['id']}</td>
                    <td>{user['username']}</td>
                    <td>{user['role']}</td>
                    <td>
                          
                        <a class="nav-link" data-url="/edit_users?id={user['id']}"  href="#"><i class="fa fa-pencil-square" aria-hidden="true"></i></a> |
                        <button onclick="Modal({user['id']})"><i class="fa fa-trash" aria-hidden="true"></i></button>
                    </td>
                </tr>

        """
          
           # HTML para o modal de confirmação
          content += """
            </table>

            <!-- Modal de confirmação -->
            <div id="deleteUserModal" class="modal">
                <div class="modal-content">
                    <span class="close" onclick="closeModal_user()">&times;</span>
                    <h2>Confirmação de Deleção</h2>
                    <p id="modalMessage">Tem certeza que deseja deletar este usuário?</p>
                    <form id="deleteForm" action="/delete_users" method="POST">
                        <input type="hidden" id="deleteUser" name="id">
                        <button type="submit">Confirmar Deleção</button>
                    </form>
                    <button onclick="closeModal_user()">Cancelar</button>
                </div>
            </div>
    """
        
         self.wfile.write(content.encode('utf-8'))
        
    #Exibir produtos
    def handle_admin_products_page(self):
    # Exibe a lista de produtos no admin com a lógica de estoque e modal de confirmação
     self.send_response(200)
     self.send_header('Content-type', 'text/html')
     self.end_headers()

     product_controller = ProductController()
     products = product_controller.list_products()
    
    
    
    
       
        
       
     
        
     content = f"""
   
            <h1>Lista de Produtos</h1>
           <a class="nav-link" data-url="/add_products" href="#"><i class="fa fa-plus" aria-hidden="true"></i></a>

            <table border="1">
                <tr>
                    <th>ID</th>
                    <th>Nome</th>
                    <th>Preço</th>
                    <th>Desconto</th>
                    <th>Categoria</th>
                    <th>Estoque</th>
                    <th>Ação</th>
                </tr>
    """

     for product in products:
        stock_status = "Sem estoque" if product['stock_quantity'] == 0 else f"Em estoque ({product['stock_quantity']})"
        content += f"""
                 
                <tr>
                    <td>{product['id']}</td>
                    <td>{product['product_name']}</td>
                    <td>R$ {product['product_price']}</td>
                    <td>R$ {product['discount_price']}</td>
                    <td>{product['categoria_id']}</td>
                    <td>{stock_status}</td>
                    <td>
                       
                      
                      <a class="nav-link" data-url="/edit_products?id={product['id']}" href="#"><i class="fa fa-pencil-square" aria-hidden="true"></i></a> | 
                     <button onclick="showModal({product['id']})"><i class="fa fa-trash" aria-hidden="true"></i></button>
                    </td>
                </tr>
        """

    # HTML para o modal de confirmação
     content += """
            </table>

            <!-- Modal de confirmação -->
            <div id="deleteModalProduct" class="modal">
                <div class="modal-content">
                    <span class="close" onclick="closeModal()">&times;</span>
                    <h2>Confirmação de Deleção</h2>
                    <p id="modalMessage">Tem certeza que deseja deletar este produto?</p>
                    <form id="deleteForm" action="/delete" method="POST">
                        <input type="hidden" id="deleteProduct" name="product_id">
                        <button type="submit">Confirmar Deleção</button>
                    </form>
                    <button onclick="closeModal()">Cancelar</button>
                </div>
            </div>

           
    """
     self.wfile.write(content.encode('utf-8'))
            
    
    #adicionar produtos
    def handle_admin_product_add_page(self):
    # Exibe o formulário para adicionar produto
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
    
    # Obtém as categorias do banco de dados
      contegorys = CetegoryController.select_category_by_products()
    
    # Inicia o conteúdo HTML
      content = """
    
    <form action="/add_product_post" method="POST" enctype="multipart/form-data" class="product-form">
    <input type="text" name="name" placeholder="Nome do Produto" required>
    <input type="text" name="price" placeholder="Preço" required>
    <input type="text" name="discount_price" placeholder="Preço com Desconto" required>
    <div id="description-container">
    <button id="add-description-btn" onclick="insertTextarea()"><i class="fas fa-pencil-alt"></i>Descrição</button>
    </div>
 
    <select name="category_id" id="category_id">
    <option value="">Selecione uma sub-subcategoria</option>
    """
    
    # Adiciona as opções de sub-subcategorias ao select
      for cat in contegorys:
        content += f"""
            <option value="{cat['sub_subcategoria_id']}">{cat['nome_categoria']}</option>
        """
    
    # Finaliza o conteúdo HTML
      content += """
        </select>
        <input type="text" name="stock" placeholder="Quantidade" required>
        <input type="file" name="product_image" required>
        <button type="submit">Adicionar Produto</button>
       
    </form>
    
"""
    
    # Envia o conteúdo HTML
      self.wfile.write(content.encode('utf-8'))
     
    #editar produtos

    def handle_admin_product_edit_page(self,product_id):    
    # Exibe o formulário para editar um produto existente
     product_controller = ProductController()
     product = product_controller.get_product_by_id(product_id)
     
     content = f"""
    <html>
        <head>
            <title>Editar Produto - Administrador</title>
        </head>
        <body>
            <h1>Editar Produto</h1>
            <form action="/edit" method="POST" enctype="multipart/form-data" class="product-form">
                <input type="hidden" name="product_id" value="{product['id']}">
                
                <label for="name">Nome do Produto:</label>
                <input type="text" id="name" name="name" value="{product['product_name']}" required><br><br>

                <label for="price">Preço:</label>
                <input type="text" id="price" name="price" value="{product['product_price']}" required><br><br>

                <label for="discount_price">Preço com Desconto:</label>
                <input type="text" id="discount_price" name="discount_price" value="{product['discount_price']}"><br><br>

                <label for="category_id">Categoria:</label>
                <input type="text" id="category_id" name="category_id" value="{product['categoria_id']}" required><br><br>

                <label for="stock">Estoque:</label>
                <input type="number" id="category_id" name="stock" value="{product['stock_quantity']}" required><br><br>
                <input type="text"  id="category_id" name="product_mark" value="{product['product_mark']}" required><br><br>

               <input type="file" name="product_image" required>
                 <div id="description-container">
                <button id="add-description-btn" onclick="insertTextarea()"><i class="fas fa-pencil-alt"></i>Descrição</button>
              
                </div>
                <button type="submit">Atualizar Produto</button>
            </form>
        </body>
    </html>
    """
     self.send_response(200)
     self.send_header('Content-type', 'text/html')
     self.end_headers()
     self.wfile.write(content.encode('utf-8'))

        #Post AdD
   
   
   #Post adicionar produtos
    def handle_admin_product_add(self):
     content_type = self.headers.get('Content-Type')
     print(f"Tipo de Conteúdo: {content_type}")

     if not content_type or not content_type.startswith('multipart/form-data'):
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b"Erro: Content-Type invalido. Use 'multipart/form-data'.")
        return

    # Parse da requisição
     form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})

    # Extrair campos do formulário
     product_name = form.getvalue('name')
     product_price = form.getvalue('price')
     discount_price = form.getvalue('discount_price')
     category_id = form.getvalue('category_id')
     stock_quantity = form.getvalue('stock')
     product_description = form.getvalue('description')

    # Extrair o arquivo de imagem
     file_field = form['product_image'] if 'product_image' in form else None

    # Verificar se o arquivo foi recebido corretamente
     product_image_path = None
     if file_field is not None and hasattr(file_field, 'filename') and file_field.filename:
        print(f"Arquivo recebido: {file_field.filename}")
        
        upload_dir = "uploads/"
        os.makedirs(upload_dir, exist_ok=True)
        file_name = os.path.basename(file_field.filename)
        file_path = os.path.join(upload_dir, file_name)

        # Salvar o arquivo de imagem
        try:
            with open(file_path, 'wb') as output_file:
                output_file.write(file_field.file.read())
            product_image_path = file_path
            print(f"Imagem salva em: {file_path}")
        except Exception as e:
            print(f"Erro ao salvar a imagem: {e}")
        product_image_path = f"http://127.0.0.1:8000/uploads/{file_name}"

            # Exemplo de logging
        print(f"URL completa da imagem: {product_image_path}")
    # Salvar os dados no banco de dados (incluindo o caminho da imagem)
     controller = ProductController()
     controller.add_product(product_name, product_price, discount_price, category_id, stock_quantity, product_image_path,product_description)

    # Redirecionamento após salvar
     self.send_response(302)
     self.send_header('Location', '/display_products')
     self.end_headers()
     #Poste Edit
    
    #Post editar produtos
    def handle_admin_product_edit(self, product_id):
     
      content_type = self.headers.get('Content-Type')
      print(f"Tipo de Conteúdo: {content_type}")

      if not content_type or not content_type.startswith('multipart/form-data'):
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b"Erro: Content-Type invalido. Use 'multipart/form-data'.")
        return

    # Parse da requisição
      form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})

    # Extrair campos do formulário
      product_id = form.getvalue('product_id')
      product_name = form.getvalue('name')
      product_price = form.getvalue('price')
      discount_price = form.getvalue('discount_price')
      category_id = form.getvalue('category_id')
      stock_quantity = form.getvalue('stock')
      product_description = form.getvalue('description')
      product_mark = form.getvalue('product_mark')
    # Extrair o arquivo de imagem
      file_field = form['product_image'] if 'product_image' in form else None

    # Verificar se o arquivo foi recebido corretamente
      product_image_path = None
      if file_field is not None and hasattr(file_field, 'filename') and file_field.filename:
        print(f"Arquivo recebido: {file_field.filename}")
        
        upload_dir = "uploads/"
        os.makedirs(upload_dir, exist_ok=True)
        file_name = os.path.basename(file_field.filename)
        file_path = os.path.join(upload_dir, file_name)

        # Salvar o arquivo de imagem
        try:
            with open(file_path, 'wb') as output_file:
                output_file.write(file_field.file.read())
            product_image_path = file_path
            print(f"Imagem salva em: {file_path}")
        except Exception as e:
            print(f"Erro ao salvar a imagem: {e}")
        product_image_path = f"http://127.0.0.1:8000/uploads/{file_name}"

            # Exemplo de logging
       # print(f"URL completa da imagem: {product_image_path}")
    # Salvar os dados no banco de dados (incluindo o caminho da imagem)
      controller = ProductController()
      controller.update_product(product_id, product_name,product_mark, product_price, discount_price, category_id, stock_quantity, product_image_path,product_description)

    # Redirecionamento após salvar
      self.send_response(302)
      self.send_header('Location', '/display_products')
      self.end_headers()

    #Poste delet
    def handle_admin_product_delete(self, product_id):
     content_length = int(self.headers['Content-Length'])
     post_data = self.rfile.read(content_length)
     data = parse_qs(post_data.decode('utf-8'))
     product_id = data.get('product_id', [None])[0]
     controller = ProductController()
     controller.delete_product(product_id)
     self.send_response(302)  # Redireciona
     self.send_header('Location', '/display_products')  # Para uma página de sucesso
     self.end_headers()
     


    #Lista de detalhes do pedido
    def handle_admin_orders_page(self):
     orders = OrderController()
     order = orders.get_all_orders()
     self.send_response(200)
     self.send_header('Content-type', 'text/html')
     self.end_headers()
     user_id = self.get_user_id_from_cookies()
     users = AdminLoginController.get_users_by_id(self,user_id)
    
     role = users["role"]
     superAdmins = AdminLoginController()
     superAdmin =superAdmins.get_users_super_by_id(role,user_id)
     for s in superAdmin:
        admin = s["role"]
        if admin == 'superadmin' or admin == 'store_admin':
         for ord in order:
          super_html = f"""
                      <a class="nav-link" data-url="/update_status?order_id={ord['order_id']}" href="#">Atualizar Status</a>  """
        
        else: 
         super_html =""  
    # Criando o conteúdo da tabela
     orders_html = ""
     for ord in order:
        orders_html += f"""
        <tr>
            <td>{ord['order_id']}</td>
            <td>{ord['first_name']}</td>
            <td>{ord['shipping_date']}</td>
            <td>{ord['order_status']}</td>
            <td>R$ {ord['total_amount']:.2f}</td>
            <td>{ord['payment_status']}</td>
           
            <td>
                {super_html}|
              
                 <a class="nav-link" data-url="/view_order?order_id={ord['order_id']}" href="#">Ver Detalhes</a> 
            </td>
        </tr>
        """

    # Montando a página HTML
     content = f"""
    <html>
        <head>
            <title>Gerenciar Pedidos</title>
        </head>
        <body>
            <h1>Lista de Pedidos</h1>
            <table border="1">
                <thead>
                    <tr>
                        <th>Nº Pedido</th>
                        <th>Cliente</th>
                        <th>Data</th>
                        <th>Status</th>
                        <th>Total</th>
                        <th>Pagamento</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {orders_html}
                </tbody>
            </table>
        </body>
    </html>
    """
     self.wfile.write(content.encode('utf-8'))
 
    #Lista de detalhes do pedido completo por id
    def details_admin_orders_page(self, order_id):
       self.send_response(200)
       self.send_header('Content-type', 'text/html')
       self.end_headers()
       orders_controll = OrderController
       order_details = orders_controll.get_order_details(order_id)
       print()
    # Aqui você pode criar a estrutura HTML para exibir os detalhes do pedido
       content = f"""
    <html>
        <head>
            <title>Detalhes do Pedido #{order_id}</title>
        </head>
        <body>
            <h1>Detalhes do Pedido #{order_id}</h1>
            <table>
                <tr>
                    <th>Nome</th>
                    <th>Email</th>
                    <th>Endereço</th>
                    <th>Data de Envio</th>
                    <th>Status do Pedido</th>
                    <th>Status do Pagamento</th>
                    <th>Produto</th>
                    <th>Quantidade</th>
                    <th>Preço</th>
                </tr>
    """

       for detail in order_details:
        address = f"{detail['street']}, {detail['city']}, {detail['state']} - {detail['zip_code']}"
        content += f"""
                <tr>
                    <td>{detail['first_name']} {detail['last_name']}</td>
                    <td>{detail['email']}</td>
                    <td>{address}</td>
                    <td>{detail['shipping_date']}</td>
                    <td>{detail['order_status']}</td>
                    <td>{detail['payment_status']}</td>
                    <td>{detail['product_name']}</td>
                    <td>{detail['quantity']}</td>
                    <td>R$ {detail['price']:.2f}</td>
                </tr>
        """

       content += """
            </table>
            <a class="nav-link" data-url="/lista_de_pedidos" href="#">Voltar à lista de pedidos</a>
        </body>
    </html>
    """
     
       self.wfile.write(content.encode('utf-8'))
      
     #pagina para atualizar o status do pedido 
    def update_status_orders_page(self,order_id):
       updates = OrderController
       updates.get_all_orders(order_id)
      
         
       content = f"""
    <form action="/update_status_order" method="POST">
     <input type="hidden" name="order_id" value="{order_id}">
    <select name="order_status">
        <option value="Pending">Pendente</option>
        <option value="Processing">Processando</option>
        <option value="Shipped">Enviado</option>
        <option value="Delivered">Entregue</option>
        <option value="Canceled">Cancelado</option>
    </select>
    <input type="submit" value="Atualizar Status">
</form>
    """
       self.send_response(200)
       self.send_header('Content-type', 'text/html')
       self.end_headers()
       self.wfile.write(content.encode('utf-8'))
    #Update do pedido
    def status_update(self,order_id):
       content_length = int(self.headers['Content-Length'])
       post_data = self.rfile.read(content_length)
       data = parse_qs(post_data.decode('utf-8'))
       order_id = data.get('order_id', [None])[0]
       order_status = data.get('order_status', [None])[0]
       updates = OrderController
       updates.update_order_status(order_id, order_status)

       self.send_response(302)  # Redireciona
       self.send_header('Location', '/lista_de_pedidos')  # Para uma página de sucesso
       self.end_headers()

   

    def report_page(self):
       content = f"""
      <h1 class="h1-form">Gerar Relatórios</h1>

<form action="/generate_report" method="POST" class="report-form">
    <label for="start_date">Data Inicial:</label>
    <input type="date" id="start_date" name="start_date" required>

    <label for="end_date">Data Final:</label>
    <input type="date" id="end_date" name="end_date" required>

    <button type="submit" class="submit-btn">Gerar Relatório</button>
</form>

<form action="/generate_report" method="POST" class="report-form">
    <label for="order_status">Por status:</label>
    <select name="order_status" id="order_status">
        <option value="Pending">Pendente</option>
        <option value="Processing">Processando</option>
        <option value="Shipped">Enviado</option>
        <option value="Delivered">Entregue</option>
        <option value="Canceled">Cancelado</option>
    </select>
    <button type="submit" class="submit-btn">Gerar Relatório</button>
</form>

 """
       
       self.send_response(200)
       self.send_header('Content-type', 'text/html')
       self.end_headers()
       self.wfile.write(content.encode('utf-8'))

    
    def generate_report_post(self):

         content_length = int(self.headers['Content-Length'])
         post_data = self.rfile.read(content_length)
         data = parse_qs(post_data.decode('utf-8'))
         start_date = data.get('start_date', [None])[0]
         order_status = data.get('order_status', [None])[0]
         end_date = data.get('end_date', [None])[0]

    # Gera o relatório
         reports = OrderController 
         status = OrderController 
         report = reports.order_report(start_date, end_date)
         report_status = status.order_report_status(order_status)
    
       
         self.send_response(200)
         self.send_header('Content-type', 'text/html')
         self.end_headers()
        
        # Exibição dos resultados do relatório
         report_html = "<h2>Relatório de Pedidos</h2>"
         report_html += "<table><tr><th>ID do Pedido</th><th>Data</th><th>Valor Total</th><th>Status</th></tr>"
         if report and "data" in report:
          for order in report["data"]:
          
           report_html += f"<tr><td>{order['order_id']}</td><td>{order['order_date']}</td><td>{order['total_amount']}</td><td>{order['order_status']}</td><td> <a href='/download_csv?status={order['order_status']}' class='btn'>Download CSV</a></td><td> <a href='/download_excel?status={order['order_status']}' class='btn'>Download Exel</a></td></tr>"
        
           report_html += "</table>"
           self.wfile.write(report_html.encode('utf-8'))
      
         else:
            print("Nenhum pedido encontrado.")
            
         if report_status and "data" in report_status:
           report_html = "<h2>Relatório de Pedidos por status</h2>"
           report_html += "<table><tr><th>Status</th><th>Total de pedidos</th><th>Valor Total</th></tr>"
            
         for order in report_status["data"]:
            report_html += f"<tr><td>{order['order_status']}</td><td>{order['total_orders']}</td><td>{order['total_value']}</td><td> <a href='/download_csv?status={order['order_status']}' class='btn'>Download CSV</a></td><td> <a href='/download_excel?status={order['order_status']}' class='btn'>Download Exel</a></td></tr>"
       
            report_html += "</table>"
            self.wfile.write(report_html.encode('utf-8'))
      



    
    # Método para lidar com o download do relatório em CSV
    def handle_download_order_report_csv(self, order_status):
        # Gera o relatório de acordo com o status
        r = OrderController
        report_data = r.order_report_status(order_status)  # Chama a função que gera o relatório
         # Para depuração

        # Define o caminho do arquivo CSV
        file_path = f"order_report_{order_status}.csv"
        
        # Escreve o relatório no arquivo CSV
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['order_status', 'total_orders', 'total_value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in report_data['data']:  # Acesse a lista de dados corretamente
                writer.writerow(row)

        # Envia o arquivo CSV como resposta
        try:
            with open(file_path, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-Type', 'text/csv')
                self.send_header('Content-Disposition', f'attachment; filename="{file_path}"')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def handle_download_order_report_excel(self, order_status):
        # Gera o relatório de acordo com o status
        r = OrderModel
        file_path =r.generate_order_report_excel(order_status)  # Chama a função que gera o Excel

        # Envia o arquivo Excel como resposta
        try:
            with open(file_path, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()


    #Add slide
    def handle_admin_product_add_slide(self):
    # Exibe o formulário para adicionar produto
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
 
        content = """

    <form action="/add_slide_post" method="POST" enctype="multipart/form-data" class="product-form">
       <input type="file" name="slide_image" required>
        <button type="submit">Adicionar Slide</button>
    </form>

"""
        self.wfile.write(content.encode('utf-8'))

    #Listar slide 
    def handle_list_slide(self):
    # Exibe a lista de produtos no admin com a lógica de estoque e modal de confirmação
     self.send_response(200)
     self.send_header('Content-type', 'text/html')
     self.end_headers()

     slide_controller = Controller_slide()
     slides = slide_controller.list_slide()
     content = f"""
    
            <h1>Lista de Produtos</h1>
            <a class="nav-link" data-url="/add_slide" href="#"><i class="fa fa-plus" aria-hidden="true"></i></a> 
            <table border="1">
                <tr>
                    <th>ID</th>
                    <th>Nome</th>
                    <th>Ação</th>
                </tr>
    """

     for sli in slides:
       
        content += f"""
                <tr>
                    <td>{sli['slide_id']}</td>
                    <td>{sli['slide_image']}</td>
                  <td>
                        
                       <a class="nav-link" data-url="/update_slides?slide_id={sli['slide_id']}" href="#"><i class="fa fa-pencil-square" aria-hidden="true"></i></a> | 
                        <button onclick="showModalSlid({sli['slide_id']})"><i class="fa fa-trash" aria-hidden="true"></i></button>
                    </td>
                </tr>
        """

    # HTML para o modal de confirmação
     content += """
            </table>

            <!-- Modal de confirmação -->
            <div id="deleteModalSlid" class="modal">
                <div class="modal-content">
                    <span class="close" onclick="closeModalSlid()">&times;</span>
                    <h2>Confirmação de Deleção</h2>
                    <p id="modalMessage">Tem certeza que deseja deletar este produto?</p>
                    <form id="deleteForm" action="/delete_slide" method="POST">
                        <input type="hidden" id="deleteSlid" name="slide_id">
                        <button type="submit">Confirmar Deleção</button>
                    </form>
                    <button onclick="closeModalSlid()">Cancelar</button>
                </div>
            </div>

            
    """
     self.wfile.write(content.encode('utf-8'))
    
    def handle_edit_slid(self,slide_id):    
    # Exibe o formulário para editar um produto existente
     slide_id_controller = Controller_slide()
     slid = slide_id_controller.get_slide_by_id(slide_id)
     
     content = f"""
    <html>
        <head>
            <title>Editar Produto - Administrador</title>
        </head>
        <body>
            <h1>Editar Produto</h1>
            <form action="/edit_slid_post" method="POST" enctype="multipart/form-data" class="product-form">
                <input type="hidden" name="slide_id" value="{slid['slide_id']}">
                 <input type="file" name="slide_image" required>
                <button type="submit">Editar Slide</button>
              
               
            </form>
        </body>
    </html>
    """
     self.send_response(200)
     self.send_header('Content-type', 'text/html')
     self.end_headers()
     self.wfile.write(content.encode('utf-8'))
    
    
    #slid_post
    def handle_admin_slide_add(self):
       content_type = self.headers.get('Content-Type')
       print(f"Tipo de Conteúdo: {content_type}")

       if not content_type or not content_type.startswith('multipart/form-data'):
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b"Erro: Content-Type invalido. Use 'multipart/form-data'.")
        return

    # Parse da requisição
       form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})

   
    

    # Extrair o arquivo de imagem
       file_field = form['slide_image'] if 'slide_image' in form else None

    # Verificar se o arquivo foi recebido corretamente
       slide_image = None
       if file_field is not None and hasattr(file_field, 'filename') and file_field.filename:
        print(f"Arquivo recebido: {file_field.filename}")
        
        upload_dir = "uploads/"
        os.makedirs(upload_dir, exist_ok=True)
        file_name = os.path.basename(file_field.filename)
        file_path = os.path.join(upload_dir, file_name)

        # Salvar o arquivo de imagem
        try:
            with open(file_path, 'wb') as output_file:
                output_file.write(file_field.file.read())
            slide_image = file_path
            print(f"Imagem salva em: {file_path}")
        except Exception as e:
            print(f"Erro ao salvar a imagem: {e}")
        slide_image = f"http://127.0.0.1:8000/uploads/{file_name}"

            # Exemplo de logging
        print(f"URL completa da imagem: {slide_image}")
    # Salvar os dados no banco de dados (incluindo o caminho da imagem)
       controller_slid = Controller_slide()
       controller_slid.add_slid(slide_image)

    # Redirecionamento após salvar
       self.send_response(302)
       self.send_header('Location', '/list_slide')
       self.end_headers()
    
    #slid_post_edite
    def handle_admin_slide_edite(self,slide_id):
       content_type = self.headers.get('Content-Type')
      
       print(f"Tipo de Conteúdo: {content_type}")

       if not content_type or not content_type.startswith('multipart/form-data'):
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b"Erro: Content-Type invalido. Use 'multipart/form-data'.")
        return
    
    # Parse da requisição
       form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})

       slide_id  = form.getvalue('slide_id')

    # Extrair o arquivo de imagem
       file_field = form['slide_image'] if 'slide_image' in form else None

    # Verificar se o arquivo foi recebido corretamente
       slide_image = None
       if file_field is not None and hasattr(file_field, 'filename') and file_field.filename:
        print(f"Arquivo recebido: {file_field.filename}")
        
        upload_dir = "uploads/"
        os.makedirs(upload_dir, exist_ok=True)
        file_name = os.path.basename(file_field.filename)
        file_path = os.path.join(upload_dir, file_name)

        # Salvar o arquivo de imagem
        try:
            with open(file_path, 'wb') as output_file:
                output_file.write(file_field.file.read())
            slide_image = file_path
            print(f"Imagem salva em: {file_path}")
        except Exception as e:
            print(f"Erro ao salvar a imagem: {e}")
        slide_image = f"http://127.0.0.1:8000/uploads/{file_name}"

            # Exemplo de logging
        print(f"URL completa da imagem: {slide_image}")
    # Salvar os dados no banco de dados (incluindo o caminho da imagem)
       controller_slid = Controller_slide()
       controller_slid.edit_slid(slide_image,slide_id)

    # Redirecionamento após salvar
       self.send_response(302)
       self.send_header('Location', '/list_slide')
       self.end_headers()

   #deletar slides
    def delet_slides(self,slide_id):
       content_length = int(self.headers['Content-Length'])
       post_data = self.rfile.read(content_length)
       data = parse_qs(post_data.decode('utf-8'))
       slide_id  = data.get('slide_id', [None])[0]
      
       delet_slide = Controller_slide()
       delet_slide.delete_slide(slide_id)
       self.send_response(302)  # Redireciona
       self.send_header('Location', '/list_slide')  # Para uma página de sucesso
       self.end_headers()
    

    #adicionar categorias
    def add_category_get(self):
       self.send_response(200)
       self.send_header('Content-type', 'text/html')
       self.end_headers()
 
       content = """

    <h1 class="h1-form">Inserir Nova Categoria</h1>
<form action="/add_category_post" method="POST" class="category-form">
    <label for="categoria_pai">Categoria Pai:</label>
    <input type="text" id="categoria_pai" name="categoria_pai" placeholder="Ex: Telefones e Celulares" required>

    <label for="subcategoria">Subcategoria:</label>
    <input type="text" id="subcategoria" name="subcategoria" placeholder="Ex: Smartphones">

    <label for="sub_subcategoria">Sub-subcategoria:</label>
    <input type="text" id="sub_subcategoria" name="sub_subcategoria" placeholder="Ex: Android">

    <button type="submit" class="submit-btn">Cadastrar Categorias</button>
</form>

"""
       self.wfile.write(content.encode('utf-8'))


    #post adicionar categorias
    def add_category_post(self):
       content_length = int(self.headers['Content-Length'])
       post_data = self.rfile.read(content_length)
       data = parse_qs(post_data.decode('utf-8'))
        
       categoria1  = data.get('categoria_pai', [None])[0]
       categoria2 = data.get('subcategoria', [None])[0]
       categoria3 = data.get('sub_subcategoria', [None])[0]
       controller = CetegoryController()
       print(categoria1, categoria2,categoria3)
       controller.add_category(categoria1, categoria2,categoria3)
       self.send_response(302)  # Redireciona
       self.send_header('Location', '/admin')  # Para uma página de sucesso
       self.end_headers()

    #Listar categorias
    def list_category_get(self):
     caterys = CetegoryController
     categry = caterys.select_category_by_products_list()
     self.send_response(200)
     self.send_header('Content-type', 'text/html')
     self.end_headers()
   
    
    
        
    
        
    # Criando o conteúdo da tabela
     orders_html = ""
     for cat in categry:
        orders_html += f"""
        <tr>
           
            <td>{cat['id_da_Categoria']}</td>
            <td>{cat['nome_da_Categoria']}</td>
            <td>{cat['nome_da_Subcategoria']}</td>
            <td>{cat['sub_subcategoria_nome']}</td>
            
           
            <td>
              <a class="nav-link" data-url="/update_categorys?cat_id={cat['id_da_Categoria']}" href="#"><i class="fa fa-pencil-square" aria-hidden="true"></i></a> | 
                    <button onclick="showModalCat({cat['id_da_Categoria']})"><i class="fa fa-trash" aria-hidden="true"></i></button>
              
                 
            </td>
        </tr>
        """

    # Montando a página HTML
     content = f"""
   
            <h1>Categorias</h1>
            <a class="nav-link" data-url="/add_category" href="#"><i class="fa fa-plus" aria-hidden="true"></i></a> 
            <table border="1">
                <thead>
                    <tr>
                         <th>Codigo</th>
                        <th>Categoria</th>
                        <th>Sub Categoria</th>
                        <th>Caracteristica do produdo</th>
                       <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {orders_html}
                </tbody>
            </table>
      
    """
     content += """
            </table>

            <!-- Modal de confirmação -->
            <div id="deleteModalCat" class="modal">
                <div class="modal-content">
                    <span class="close" onclick="closeModalCat()">&times;</span>
                    <h2>Confirmação de Deleção</h2>
                    <p id="modalMessage">Tem certeza que deseja deletar este produto?</p>
                    <form id="deleteForm" action="/delete_cat" method="POST">
                        <input type="hidden" id="deleteCat" name="cat_id">
                        <button type="submit">Confirmar Deleção</button>
                    </form>
                    <button onclick="closeModalCat()">Cancelar</button>
                </div>
            </div>

            
    """
     self.wfile.write(content.encode('utf-8'))


    def handle_admin_category_edit_page(self,cat_id):
     
    # Exibe o formulário para editar um produto existente
     cats = CetegoryController
     cat = cats.select_category_by_edits(cat_id)
     for c in cat:
      content = f"""
      <h1 class="h1-form">Editar Categoria</h1>
    <form action="/update_cat" method="POST" class="category-form">
      <!-- Campo oculto para o ID da categoria a ser editada -->
    <input type="hidden" name="cat_id" value="{c['id_da_Categoria']}">

    <!-- Campo para selecionar o nível de edição -->
    <label for="edit_level">Nível de Edição:</label>
    <select id="edit_level" name="edit_level" required>
        <option value="categoria">Somente Categoria</option>
        <option value="subcategoria">Somente Subcategoria</option>
        <option value="sub_subcategoria">Somente Sub-subcategoria</option>
        <option value="todas">Todas as Categorias e Subcategorias</option>
    </select>

    <!-- Campo para editar o nome da categoria -->
    <label for="new_category_name">Nome da Categoria:</label>
    <input type="text" id="new_category_name" name="new_category_name" value="{c['nome_da_Categoria']}" placeholder="Nome da Categoria" required>

    <!-- Campo para editar o nome da subcategoria -->
    <label for="new_subcategory_name">Nome da Subcategoria:</label>
    <input type="text" id="new_subcategory_name" name="new_subcategory_name" value="{c['nome_da_Subcategoria']}" placeholder="Nome da Subcategoria">

    <!-- Campo para editar o nome da sub-subcategoria -->
    <label for="new_sub_subcategory_name">Nome da Sub-subcategoria:</label>
    <input type="text" id="new_sub_subcategory_name" name="new_sub_subcategory_name" value="{c['sub_subcategoria_nome']}" placeholder="Nome da Sub-subcategoria">

    <button type="submit">Salvar Alterações</button>
</form>
    """
     self.send_response(200)
     self.send_header('Content-type', 'text/html')
     self.end_headers()
     self.wfile.write(content.encode('utf-8'))


    def handle_update_category(self,cat_id):
       content_length = int(self.headers['Content-Length'])
       post_data = self.rfile.read(content_length)
       data = parse_qs(post_data.decode('utf-8'))
       cat_id = data.get('cat_id', [None])[0]
       edit_level = data.get('edit_level', [None])[0]
       new_category_name = data.get('new_category_name', [None])[0]
       new_subcategory_name = data.get('new_subcategory_name', [None])[0]
       new_sub_subcategory_name = data.get('new_sub_subcategory_name', [None])[0]
       updates = CetegoryController
       updates.update_category(edit_level,new_category_name,new_subcategory_name,new_sub_subcategory_name,cat_id)

       self.send_response(302)  # Redireciona
       self.send_header('Location', '/lista_de_pedidos')  # Para uma página de sucesso
       self.end_headers()


    def delet_category(self,cat_id):
     
       content_length = int(self.headers['Content-Length'])
       post_data = self.rfile.read(content_length)
       data = parse_qs(post_data.decode('utf-8'))
       cat_id  = data.get('cat_id', [None])[0]
      
       delet_cat = CetegoryController()
       delet_cat.delete_cat(cat_id)
       self.send_response(302)  # Redireciona
       self.send_header('Location', '/list_slide')  # Para uma página de sucesso
       self.end_headers()
    



    def handle_404(self):
        # Manipula requisições para rotas inexistentes
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")

    def _render_template(self, template_name, context=None):
        if context is None:
            context = {}  # Garantindo que context não seja None

        try:
            # Lê o arquivo HTML do template
            with open(f'admin_views/{template_name}.html', 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Substitui as variáveis do contexto no conteúdo do HTML
            for key, value in context.items():
                html_content = html_content.replace(f'{{{{ {key} }}}}', str(value))

            return html_content
        except FileNotFoundError:
            return None
        
#conexão com servidor
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servindo na porta {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
    