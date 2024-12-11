from admin_model.category import Category

class CetegoryController:
 @staticmethod
 def add_category(categoria1, categoria2,categoria3):
        Category.add_category(categoria1, categoria2,categoria3)
 
 def select_category_by_products():
     category = Category.select_category_by_products()
     return [
            {
                "nome_categoria": cat["sub_subcategoria_nome"],
                "sub_subcategoria_id": cat["sub_subcategoria_id"],
                
            }
            for cat in category
        ]
 def select_category_by_products_list():
     category = Category.select_category_by_products()
     
     return [
            {
                "id_da_Categoria": cat["ID_da_Categoria"],
                "id_categoria_pai": cat["id_categoria_pai"],
                "nome_da_Categoria": cat["Nome_da_Categoria"],
                "nome_da_Subcategoria": cat["Nome_da_Subcategoria"],
                "sub_subcategoria_nome": cat["sub_subcategoria_nome"],
                
            }
            for cat in category
        ]
 def select_category_by_edits(id_categoria):
     category = Category.select_category_by_edits(id_categoria)
     
     return [
            {
                "id_da_Categoria": cat["ID_da_Categoria"],
                "nome_da_Categoria": cat["Nome_da_Categoria"],
                "nome_da_Subcategoria": cat["Nome_da_Subcategoria"],
                "sub_subcategoria_nome": cat["sub_subcategoria_nome"],
                
            }
            for cat in category
        ]
 
 def update_category(edit_level,new_category_name,new_subcategory_name,new_sub_subcategory_name,cat_id):
      Category.update_categoria(edit_level,new_category_name,new_subcategory_name,new_sub_subcategory_name,cat_id)

 def delete_cat(self, cat_id):
       
        Category.delete_cat(cat_id)