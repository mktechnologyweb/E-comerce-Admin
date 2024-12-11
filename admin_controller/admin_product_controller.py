from admin_model.product import ProductModel


class ProductController:
    def list_products(self):
        products = ProductModel.list_products()
        return [
            {
                "id": product["product_id"],
                "product_name": product["product_name"],
                "product_price": product["product_price"],
                "discount_price": product["discount_price"],
                "product_rating": product["product_rating"],
                "stock_quantity": product["stock_quantity"],
                "categoria_id": product["id_categoria"],
                "images": product["product_image"]
            }
            for product in products
        ]
    

    def get_product_by_id(self, product_id):
        product = ProductModel.get_product_by_id(product_id)
        if product:
            return {
                "id": product["product_id"],
                "product_name": product["product_name"],
                "product_price": product["product_price"],
                "discount_price": product["discount_price"],
                "product_rating": product["product_rating"],
                "stock_quantity": product["stock_quantity"],
                "categoria_id": product["id_categoria"],
                "product_description": product["product_description"],
                "product_mark": product["product_mark"],
                "product_image": product["product_image"]
            }
        return None



    def add_product(self, name, price, discount_price, category_id, stock_quantity, product_image_path,product_description):
        ProductModel.add_product(name, price, discount_price, category_id, stock_quantity, product_image_path,product_description)

    def update_product(self, product_id, name,product_mark, price, discount_price, category_id, stock_quantity,product_description, product_image_path):
        ProductModel.update_product(product_id, name,product_mark, price, discount_price, category_id,stock_quantity,product_description,product_image_path)

    def delete_product(self, product_id):
        ProductModel.delete_product(product_id)

    def check_stock(self, product_id):
        return ProductModel.check_stock(product_id)
