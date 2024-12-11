import mysql.connector
from config_app.config import DB_CONFIG


class Slide:
    @staticmethod
    def add_slid(slide_image):
        conn = mysql.connector.connect(**DB_CONFIG)
        print("kkk",slide_image)
        cursor = conn.cursor()
        
        query = """
        INSERT INTO promotional_slide (slide_image) 
        VALUES (%s)
        """
        
        cursor.execute(query, (slide_image,))
        conn.commit()

        cursor.close()
        conn.close()

    @staticmethod
    def get_slide_by_id(slide_id):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT slide_id, slide_image FROM promotional_slide WHERE slide_id = %s"
        cursor.execute(query, (slide_id,))
        slide = cursor.fetchone()
        cursor.close()
        conn.close()
        return slide
    @staticmethod
    def list_slides():
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT slide_image,slide_id  FROM promotional_slide")
        slide_image = cursor.fetchall()

        cursor.close()
        conn.close()
        return slide_image


    def edit_slid(slide_id,slide_image):
        conn = mysql.connector.connect(**DB_CONFIG)
        
        cursor = conn.cursor()
        
        query = """
        UPDATE promotional_slide 
        SET slide_image = %s WHERE slide_id = %s
        """
        cursor.execute(query, (slide_id,slide_image))
        conn.commit()

        cursor.close()
        conn.close()
       
    @staticmethod
    def delete_slide(slide_id):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = "DELETE FROM promotional_slide WHERE slide_id = %s"
        cursor.execute(query, (slide_id,))
        conn.commit()

        cursor.close()
        conn.close()