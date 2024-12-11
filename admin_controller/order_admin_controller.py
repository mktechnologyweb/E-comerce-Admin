from admin_model.order import OrderModel

class OrderController:
     
     def get_all_orders(self):
        orders = OrderModel.get_all_orders(self)
        return [
            {
                "order_id": order["order_id"],
                "first_name": order["first_name"],
                "shipping_date": order["shipping_date"],
                "order_status": order["order_status"],
                "total_amount": order["total_amount"],
                "payment_status": order["payment_status"],
                
            }
            for order in orders
        ]
    

     def get_order_details(self):
        order_details = OrderModel.get_order_details(self)
        return [
            {
                "order_id": order["order_id"],
                "shipping_date": order["shipping_date"],
                "order_status": order["order_status"],
                "total_amount": order["total_amount"],
                "payment_status": order["payment_status"],
                "first_name": order["first_name"],
                "last_name": order["last_name"],
                "email": order["email"],
                "street": order["street"],
                "city": order["city"],
                "state": order["state"],
                "zip_code": order["zip_code"],
                "product_name": order["product_name"],
                "quantity": order["quantity"],
                "price": order["price"],
                
            }
            for order in order_details
        ]
    

     def update_order_status(order_id,order_status):
          OrderModel.update_order_status(order_status,order_id)

    
     def order_report(start_date, end_date):
        orders = OrderModel.generate_order_report_by_date(start_date, end_date)
        return orders
   
     
     def order_report_status(order_status):
        status = OrderModel.generate_order_report_by_status(order_status)
        return status
    
     
   
    