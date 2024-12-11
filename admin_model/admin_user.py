import bcrypt
import mysql.connector
from config_app.config import DB_CONFIG

class UserAdminModel:
    def __init__(self):
        self.connection = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()

    def create_superadmin(self, username, password,role):
        # Hasheando a senha
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Inserindo o superadmin no banco de dados
        query = "INSERT INTO usuarios_admin (username, password, role) VALUES (%s, %s, %s)"
        try:
            self.cursor.execute(query, (username, hashed_password, role))
            self.connection.commit()
            return {"status": "success", "message": "Superadmin criado com sucesso!"}
        except mysql.connector.Error as err:
            return {"status": "error", "message": str(err)}

    def close_connection(self):
        self.cursor.close()
        self.connection.close()





    def authenticate(self, username, password):
     query = "SELECT id, password, role FROM usuarios_admin WHERE username = %s"
     self.cursor.execute(query, (username,))
     result = self.cursor.fetchone()
    
     if result:
        user_id, hashed_password, role = result
       
        # A senha hasheada deve estar em bytes para a verificação
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return {"id": user_id, "role": role}

     return None


    def list_users_admin(self):
         conn = mysql.connector.connect(**DB_CONFIG)
         cursor = conn.cursor(dictionary=True)
        
         cursor.execute("SELECT  id, username , role FROM usuarios_admin")
         Users_admin = cursor.fetchall()

         cursor.close()
         conn.close()
         return Users_admin
    


    @staticmethod
    def get_users_by_id(id):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT id, username, password, role FROM usuarios_admin WHERE id = %s"
        cursor.execute(query, (id,))
        users = cursor.fetchone()

        cursor.close()
        conn.close()
        return users
    
    @staticmethod
    def get_users_super_by_id(role,id):
       
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT id, username, password, role FROM usuarios_admin WHERE id = %s AND role = %s"
        cursor.execute(query, (id,role))
        users = cursor.fetchall()

        cursor.close()
        conn.close()
        return users

    @staticmethod
    def update_user(id, username, password, role):
        
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        if password:
        
         hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
         
         query = """
         UPDATE usuarios_admin 
         SET username = %s, password = %s, role = %s
         WHERE id = %s
         """
        
         cursor.execute(query,(username, hashed_password, role, id))
        else:
        # Se a senha não for fornecida, atualize apenas o username e role
         query = """
         UPDATE usuarios_admin 
         SET username = %s, role = %s
         WHERE id = %s
        """

         cursor.execute(query,(username, hashed_password, role,id))
        try:
         cursor.execute(query,(username, hashed_password, role,id))
         conn.commit()
         return {"status": "success", "message": "Usuário atualizado com sucesso!"}
        except mysql.connector.Error as err:
         return {"status": "error", "message": str(err)}
        finally:
         cursor.close()
         conn.close()  
   
    @staticmethod
    def delete_user(id):
       
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "DELETE FROM usuarios_admin WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()

        cursor.close()
        conn.close()