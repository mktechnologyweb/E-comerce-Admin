from admin_model.admin_user import UserAdminModel

class AdminLoginController:
    def __init__(self):
        self.model = UserAdminModel()


    def create_superadmin(self, username, password, role):
        print("admin", username, password, role)
        # Chamando o método do modelo para criar o superadmin
        response = self.model.create_superadmin(username, password,role)
        return response

    #Criar super usuario manualmente
    #username = 'admin'
    #password = 'senha123'
    #hashed_password = hash_password(password)



    def login(self, request):
        username = request['get']('username')
        password = request['get']('password')
       
        # Autentica o usuário
        user = self.model.authenticate(username, password)

        if user:
            return {"status": "success", "user_id": user["id"], "role": user["role"]}
        else:
            return {"status": "error", "message": "Usuário ou senha inválidos."}

    def logout(self, request):
        # Remove o usuário da sessão
        request['session'].clear()
        return {"status": "success", "message": "Logout realizado com sucesso"}



    def list_users_admin(self):
        Users_admin = UserAdminModel.list_users_admin(self)
        return [
            {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"],
                
            }
            for user in Users_admin
        ]
    


    def get_users_by_id(self, id):
        users = UserAdminModel.get_users_by_id(id)
        if users:
            return {
                "id": users["id"],
                "username": users["username"],
                "password": users["password"],
                "role": users["role"],
               
            }
        return None
    def get_users_super_by_id(self,role, id):
        users = UserAdminModel.get_users_super_by_id(role,id)
       
        return [{
                "id": u["id"],
                "username": u["username"],
                "password": u["password"],
                "role": u["role"],
               
            } for u in users]
    
    


    def update_users(self, id, username , password, role):
        UserAdminModel.update_user(id,username, password ,role)

    def delete_user(self, id):
        UserAdminModel.delete_user(id)