from admin_model.slide import Slide


class Controller_slide:

 def add_slid(self,slide_image):
        Slide.add_slid(slide_image)

 def list_slide(self):
        slide_image = Slide.list_slides()
        return [
            {
                "slide_id": slid["slide_id"],
                "slide_image": slid["slide_image"],
              
            }
            for slid in slide_image
        ]

 def get_slide_by_id(self, slide_id):
        slide = Slide.get_slide_by_id(slide_id)
        if slide:
            return {
                "slide_id": slide["slide_id"],
                "slide_image": slide["slide_image"],
             
            }
        return None

 def edit_slid(self,slide_id,slide_image):
        Slide.edit_slid(slide_id,slide_image)

 def delete_slide(self, slide_id):
        Slide.delete_slide(slide_id)