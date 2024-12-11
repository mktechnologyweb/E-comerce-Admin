from admin_model.product import ProductModel
from admin_model.costumer import Costumer
from admin_model.order import OrderModel

class DashboardController:
    def __init__(self):
        self.product_model = ProductModel()
        self.order_model = OrderModel()
        self.user_admin_model = Costumer()

    def get_dashboard_data(self):
        total_products = self.get_total_products()
        total_orders = self.get_total_orders()
        total_users = self.get_total_users()
        
        return {
            "total_products": total_products,
            "total_orders": total_orders,
            "total_users": total_users
        }

    def get_total_products(self):
        return self.product_model.count_products()

    def get_total_orders(self):
        return self.order_model.count_orders()

    def get_total_users(self):
        return self.user_admin_model.count_users()
