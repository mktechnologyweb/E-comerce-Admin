import mysql.connector
from config_app.config import DB_CONFIG


class Category:
    @staticmethod
    def get_categoria_id(nome_categoria):
       #"""Retorna o id_categoria baseado no nome da categoria."""
     if not nome_categoria:
        raise ValueError("O nome da categoria não pode ser None ou vazio.")
     try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
       
        query = "SELECT id_categoria FROM categorias WHERE TRIM(nome_categoria) = %s"
        cursor.execute(query, (nome_categoria.strip(),))
        result = cursor.fetchone()
        # Se a categoria já existir, retorna o id_categoria
        if result:
            return result[0]
         # Caso contrário, insere a categoria e retorna o novo id_categoria
        insert_query = "INSERT INTO categorias (nome_categoria) VALUES (%s)"
        cursor.execute(insert_query, (nome_categoria,))
        conn.commit()
        # Retorna o id_categoria recém-criado
        return cursor.lastrowid
     except mysql.connector.Error as error:
        print(f"Erro ao verificar ou criar categoria: {error}")
        return None
       
    
     finally:
            cursor.close()
            conn.close()


    @staticmethod
    def add_category(categoria1, categoria2=None, categoria3=None):
        
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        id_categoria_pai1  = Category.get_categoria_id(categoria1)
               
        # Nível 2: Verifica ou cria a segunda categoria, se fornecida
        if categoria2:
            id_categoria_pai2 = Category.get_categoria_id(categoria2)
            update_query2 = "UPDATE categorias SET id_categoria_pai = %s WHERE id_categoria = %s"
            cursor.execute(update_query2, (id_categoria_pai1, id_categoria_pai2))
            conn.commit()

        # Nível 3: Verifica ou cria a terceira categoria, se fornecida
        if categoria3:
            id_categoria_pai3 =  Category.get_categoria_id(categoria3)
            insert_query3 = """
                UPDATE categorias SET id_categoria_pai = %s WHERE id_categoria = %s
            """
            cursor.execute(insert_query3, (id_categoria_pai2, id_categoria_pai3))
            conn.commit()

        print(f"Hierarquia inserida: {categoria1}, {categoria2}, {categoria3}")

       
        

        cursor.close()
        conn.close()

    @staticmethod
    def select_category_by_products():
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        query = """
    SELECT 
    c.id_categoria AS "ID_da_Categoria",
    c.id_categoria_pai AS "id_categoria_pai",
    c.nome_categoria AS "Nome_da_Categoria",
    s.id_categoria AS "ID_da_Subcategoria",
    s.nome_categoria AS "Nome_da_Subcategoria",
    ss.id_categoria AS "sub_subcategoria_id",
    ss.nome_categoria AS "sub_subcategoria_nome"
FROM 
    categorias c
LEFT JOIN 
    categorias s ON c.id_categoria = s.id_categoria_pai
LEFT JOIN 
    categorias ss ON s.id_categoria = ss.id_categoria_pai
WHERE 
    c.id_categoria_pai IS NULL  -- Para pegar apenas as categorias principais
ORDER BY 
    c.id_categoria, s.id_categoria, ss.id_categoria;"""
        cursor.execute(query,)
        category = cursor.fetchall()

        cursor.close()
        conn.close()
        
        return category
    def select_category_by_edits(id_categoria):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        query = """
    SELECT 
    c.id_categoria AS "ID_da_Categoria",
    c.nome_categoria AS "Nome_da_Categoria",
    s.id_categoria AS "ID_da_Subcategoria",
    s.nome_categoria AS "Nome_da_Subcategoria",
    ss.id_categoria AS "sub_subcategoria_id",
    ss.nome_categoria AS "sub_subcategoria_nome"
FROM 
    categorias c
LEFT JOIN 
    categorias s ON c.id_categoria = s.id_categoria_pai
LEFT JOIN 
    categorias ss ON s.id_categoria = ss.id_categoria_pai
WHERE 
    c.id_categoria_pai IS NULL  AND c.id_categoria = %s -- Para pegar apenas as categorias principais
ORDER BY 
    c.id_categoria, s.id_categoria, ss.id_categoria;"""
        cursor.execute(query,(id_categoria,))
        category = cursor.fetchall()

        cursor.close()
        conn.close()
        
        return category
    

    def delete_cat(cat_id):
       
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
    DELETE FROM categorias 
    WHERE id_categoria_pai IN (SELECT id_categoria FROM categorias WHERE id_categoria_pai = %s)
""", (cat_id,))

# Deletar subcategorias
        cursor.execute("""
    DELETE FROM categorias 
    WHERE id_categoria_pai = %s
""", (cat_id,))

# Deletar categoria principal
        cursor.execute("""
    DELETE FROM categorias 
    WHERE id_categoria = %s
""", (cat_id,))
        conn.commit()

        cursor.close()
        conn.close()


    def update_categoria(edit_level,new_category_name,new_subcategory_name,new_sub_subcategory_name,cat_id):
     conn = mysql.connector.connect(**DB_CONFIG)
     cursor = conn.cursor()
     if edit_level == 'categoria':
        novo_nome = new_category_name
        query = "UPDATE categorias SET nome_categoria = %s WHERE id_categoria = %s"
        cursor.execute(query, (novo_nome, cat_id))
     elif edit_level == 'subcategoria':
        novo_nome = new_subcategory_name
        query = "UPDATE categorias SET nome_categoria = %s WHERE id_categoria_pai = %s"
        cursor.execute(query, (novo_nome, cat_id))
     elif edit_level == 'sub_subcategoria':
        novo_nome = new_sub_subcategory_name
        query = """
        UPDATE categorias SET nome_categoria = %s 
        WHERE id_categoria_pai IN (SELECT id_categoria FROM categorias WHERE id_categoria_pai = %s)
        """
        cursor.execute(query, (novo_nome, cat_id))
     elif edit_level == 'todas':
    # Atualiza a categoria principal
      query1 = "UPDATE categorias SET nome_categoria = %s WHERE id_categoria = %s"
      cursor.execute(query1, (new_category_name, cat_id))

    # Atualiza a subcategoria
      query2 = "UPDATE categorias SET nome_categoria = %s WHERE id_categoria_pai = %s"
      cursor.execute(query2, (new_subcategory_name, cat_id))

    # Atualiza a sub-subcategoria
      query3 = """
    UPDATE categorias
    SET nome_categoria = %s
    WHERE id_categoria_pai IN (
        SELECT id_categoria FROM categorias WHERE id_categoria_pai = %s
    )
    """
      cursor.execute(query3, (new_sub_subcategory_name, cat_id))

# Confirma as mudanças no banco de dados

    
     conn.commit()
     print("Categoria atualizada com sucesso.")