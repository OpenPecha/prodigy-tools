from PIL import Image
import os

class modify_image:
    '''Different operation onto an individual image'''
    def __init__(self, im, key, degree=2):
        self.image = im
        self.key = key
        self.degree = degree
    
    def compress_image(self):
        '''Compressing the image'''
        self.image.resize((self.image.size[0]//self.degree, self.image.size[1]//self.degree))
    
    def _get_title(self):
        '''Getting the image filename'''
        title = self.key.split('/')
        return title[-1]
    
    def _remove_extension_dot(self,title):
        '''Remove the dot extension and convert it to _tif'''
        return title.replace(".", "_")
    
    def _rename_file(self):
        '''Rename the file to with the extension .jpg'''
        name = self._get_title()
        name = self._remove_extension_dot(name)
        name = f"{name}_{self.degree}.jpg"
        return name
    
    def save_image(self):
        '''Save the image with changed fileName'''
        try:
            filename = self._rename_file()
            img = self.image.save(filename)
            return filename
        except ValueError as e:
            print(e)
    
    def delete_image(self):
        '''Delete the file after prodigy has reading teh data'''
        name = self._rename_file()
        path = os.getcwd()+"/"+name

        if os.path.exists(path):
            os.remove(name)
        else:
            print("File doesnt exist")
        
    