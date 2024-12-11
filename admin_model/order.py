import json
import mysql.connector 
from config_app.config import DB_CONFIG
from openpyxl import Workbook
import csv
class OrderModel:
    def __init__(self):
        self.connection = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()

    def count_orders(self):
        query = "SELECT COUNT(*) FROM orders"  # Ajuste o nome da tabela conforme necessário
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def close_connection(self):
        self.cursor.close()
        self.connection.close()


    def get_all_orders(self):
     conn = mysql.connector.connect(**DB_CONFIG)
     cursor = conn.cursor(dictionary=True)
    
     query = """
   SELECT
    orders.order_id,
    customer.first_name,
    orders.shipping_date,
    orders.order_status,
    orders.total_amount,
    payments.payment_status
    
FROM
    orders
JOIN customer ON orders.customer_id = customer.customer_id
JOIN payments ON orders.cart_id = payments.order_id;
    
    """
    
     cursor.execute(query)
     orders = cursor.fetchall()
    
     cursor.close()
     conn.close()
    
     return orders
    


    def get_order_details(order_id):
     conn = mysql.connector.connect(**DB_CONFIG)
     cursor = conn.cursor(dictionary=True)

     query = """
   SELECT 
    orders.order_id, 
    orders.shipping_date, 
    orders.order_status, 
    orders.total_amount,
    payments.payment_status,
    customer.first_name, 
    customer.last_name, 
    customer.email,
    address.street, 
    address.city, 
    address.state, 
    address.zip_code,
    product.product_name, 
    order_item.quantity, 
    order_item.price
FROM orders
JOIN customer ON orders.customer_id = customer.customer_id
JOIN payments ON orders.cart_id = payments.order_id 
JOIN address ON orders.customer_address_id = address.address_id
JOIN order_item ON orders.order_id = order_item.order_id
JOIN product ON order_item.product_id = product.product_id
WHERE orders.order_id = %s;
    """
    
     cursor.execute(query, (order_id,))
     order_details = cursor.fetchall()
     cursor.close()
     conn.close()

     return order_details
    
    def update_order_status(order_id, order_status):
     conn = mysql.connector.connect(**DB_CONFIG)
     cursor = conn.cursor()

     query = """
    UPDATE orders 
    SET order_status = %s 
    WHERE order_id = %s
    """
     try:
        cursor.execute(query, (order_id,order_status))
        conn.commit()
        return {"status": "success", "message": "Status do pedido atualizado com sucesso!"}
     except mysql.connector.Error as err:
        return {"status": "error", "message": str(err)}
     finally:
        cursor.close()
        conn.close()


    def generate_order_report_by_date(start_date, end_date):
      conn = mysql.connector.connect(**DB_CONFIG)
      cursor = conn.cursor(dictionary=True)

      query = """
    SELECT order_id, order_date, total_amount, order_status,shipping_date
    FROM orders
    WHERE order_date BETWEEN %s AND %s
    ORDER BY order_date DESC
    """
      
    
     
      cursor.execute(query, (start_date, end_date))
      orders = cursor.fetchall()
      cursor.close()
      conn.close()
      return {"data": orders} if orders else {"data": []}
   


    def generate_order_report_by_status(order_status):
      conn = mysql.connector.connect(**DB_CONFIG)
      cursor = conn.cursor(dictionary=True)

      query = """
        SELECT 
    order_status, 
    COUNT(order_id) AS total_orders, 
    SUM(total_amount) AS total_value
    FROM orders
    WHERE order_status = %s
    GROUP BY order_status;
    """
     
      cursor.execute(query, (order_status,))
      status = cursor.fetchall()
      cursor.close()
      conn.close()
      return {"data": status} if status else {"data": []}
    


    def generate_order_report_excel(order_status):
     conn = mysql.connector.connect(**DB_CONFIG)
     cursor = conn.cursor(dictionary=True)

     query = """
        SELECT 
            order_status, 
            COUNT(order_id) AS total_orders, 
            SUM(total_amount) AS total_value
        FROM orders
        WHERE order_status = %s
        GROUP BY order_status;
    """
    
     cursor.execute(query, (order_status,))
     status = cursor.fetchall()
     cursor.close()
     conn.close()
    
    # Cria um arquivo Excel
     wb = Workbook()
     ws = wb.active
     ws.title = "Relatório de Pedidos"

    # Adiciona cabeçalhos
     ws.append(['Order Status', 'Total Orders', 'Total Value'])

    # Adiciona os dados
     for row in status:
        ws.append([row['order_status'], row['total_orders'], row['total_value']])

     # Define o caminho do arquivo Excel
     file_path = f"order_report_{order_status}.xlsx"
     wb.save(file_path)

     return file_path 
    

    def generate_order_report_by_dates(start_date, end_date=None):
     conn = mysql.connector.connect(**DB_CONFIG)
     cursor = conn.cursor(dictionary=True)

    # Consulta para selecionar dados de pedidos com base nas datas
     query = """
        SELECT 
            DATE(orders.order_date) AS order_date, 
            COUNT(orders.order_id) AS total_orders, 
            SUM(orders.total_amount) AS total_value
        FROM orders
        WHERE DATE(orders.order_date) >= %s
    """
    
     params = [start_date.split(" ")[0]]  # Pega apenas a data, ignorando a hora
    
     if end_date:
        query += " AND DATE(orders.order_date) <= %s"
        params.append(end_date.split(" ")[0])  # Pega apenas a data, ignorando a hora

     query += " GROUP BY DATE(orders.order_date)"
    
     cursor.execute(query, params)
     result = cursor.fetchall()
     cursor.close()
     conn.close()
    
     return result
    
    
    def generate_order_report_payments():
     conn = mysql.connector.connect(**DB_CONFIG)
     cursor = conn.cursor(dictionary=True)

    # Consulta para selecionar dados de pedidos com base nas datas
     query = """
    SELECT 
        DATE(payment_date) AS sale_date, 
        COUNT(*) AS total_sales, 
        SUM(CASE WHEN payment_status = 'Sucesso' THEN 1 ELSE 0 END) AS successful_sales,
        SUM(amount) AS total_amount
    FROM 
        payments
    GROUP BY 
        DATE(payment_date)
    ORDER BY 
        sale_date DESC;
    """
    
     cursor.execute(query)
     result = cursor.fetchall()

    

     for item in result:
        item['sale_date'] = item['sale_date'].strftime('%Y-%m-%d')  # Converter data para string
        item['total_sales'] = int(item['total_sales'])  # Garante que total_sales seja um inteiro
        item['successful_sales'] = int(item['successful_sales'])  # Garante que successful_sales seja um inteiro
        item['total_amount'] = float(item['total_amount']) if item['total_amount'] is not None else 0.0  # Converte Decimal para float ou define como 0.0

     total_sales = sum(item['total_sales'] for item in result)
     successful_sales = sum(item['successful_sales'] for item in result)
     total_amount = sum(item['total_amount'] for item in result)

    # Adiciona a linha de totais
     result.append({
        "sale_date": "Total Geral",
        "total_sales": total_sales,
        "successful_sales": successful_sales,
        "total_amount": total_amount
    })

     cursor.close()
     conn.close()

     return result