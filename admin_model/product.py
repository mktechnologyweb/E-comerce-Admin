import mysql.connector
from config_app.config import DB_CONFIG

class ProductModel:
    def __init__(self):
        self.connection = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()

    def count_products(self):
        query = "SELECT COUNT(*) FROM product"  # Ajuste o nome da tabela conforme necessário
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    @staticmethod
    def list_products():
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT product_id, product_name, product_price, discount_price,stock_quantity, product_image,product_rating,id_categoria FROM product")
        products = cursor.fetchall()

        cursor.close()
        conn.close()
        return products



    @staticmethod
    def add_product(name, price, discount_price, category_id, stock_quantity,product_description, product_image_path):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        query = """
        INSERT INTO product (product_name, product_price, discount_price, id_categoria, stock_quantity, product_image,product_rating,product_description) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        product_rating = "0"
        cursor.execute(query, (name, price, discount_price, category_id, stock_quantity, product_image_path, product_rating,product_description))
        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def update_product(product_id, name,product_mark, price, discount_price, category_id, stock_quantity,product_description, product_image_path):
        print("chega",product_id, name,product_mark, price, discount_price, category_id, stock_quantity,product_description, product_image_path)
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
       
        query = """
        UPDATE product 
        SET product_name = %s,product_mark = %s, product_price = %s, discount_price = %s, id_categoria = %s, stock_quantity = %s,product_image =%s, product_description= %s 
        WHERE product_id = %s
        """
        cursor.execute(query, (name,product_mark, price, discount_price, category_id, stock_quantity,product_description, product_image_path,product_id))
        conn.commit()
        
        cursor.close()
        conn.close()

    @staticmethod
    def delete_product(product_id):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "DELETE FROM product WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def check_stock(product_id):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT stock_quantity FROM product WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()

        cursor.close()
        conn.close()

        if product and product['stock_quantity'] == 0:
            return "Sem estoque"
        return "Em estoque"
    
    @staticmethod
    def get_product_by_id(product_id):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT product_id, product_name,product_mark, product_price,product_description, discount_price,stock_quantity,id_categoria, product_image, product_rating FROM product WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()

        cursor.close()
        conn.close()
        return product