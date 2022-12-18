from PIL import Image
import os
import io
import mozjpeg_lossless_optimization

class modify_image:
    '''Different operation onto an individual image'''
    def __init__(self, im, key):
        self.image = im
        self.key = key
    
    def resize_image(self):
        '''Compressing the image'''
        compressed =self.image.thumbnail(size=(1000, 700),resample = Image.Resampling.LANCZOS)
    
    def progressive_encoding(self):
        """Encode the image in progressive so that it will load better in the website"""
        pass
    
    def subsampling(self):
        """Decrease the size of image by down grading the color sample"""
        pass 

    def compress_image(self):
        byte_array = io.BytesIO()
        self.image.save(byte_array,format="JPEG")
        op_image = mozjpeg_lossless_optimization.optimize(byte_array)
        self.image = Image.open(op_image)
        self.image.save("output")

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
            image_bytes_arr = io.BytesIO()
            self.image.save(image_bytes_arr,format="JPEG")
            return image_bytes_arr
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
        
    