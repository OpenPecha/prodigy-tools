from PIL import Image
import math
import os 

class pil_image:
    '''
    compress the image using PIL library 
    
    '''
    def __init__(self, im):
        self.im = im
    
    def cal_aspect_ratio(self):
        '''
            By using the width and height of the image 
            calculating the aspect ratio of the image

            returned 
            ---------
            The updated aspect ratio of the image

        '''
        im_wd = self.im.size[0]
        im_hg = self.im.size[1]
        as_ratio = im_wd/im_hg
        return as_ratio
    
    def update_dim(self):
        '''
            Decrease the size of image by 30% from both width 
            height 

            returned 
            -------
            new updated width
            new updated height

        '''
        up_wd = self.im.size[0] * 0.3
        up_hg = self.im.size[1] * 0.3
        return (math.floor(up_wd), math.floor(up_hg))
    

    def resize_dim(self):
        dim=self.update_dim()
        resized_im = self.im.resize(dim)
        return resized_im


        


if __name__ == "__main__":
    im = Image.open("wedding.jpg")
    obj = pil_image(im)
    resized = obj.resize_dim()
    print("#"*50)
    print("Before resize the image")
    print(im.size)
    print(im.mode)
    # print(os.stat(im).st_size)
    print("#"*50)
    print("Before resize the image")
    print(resized.size)
    print(resized.mode)
    # print(os.stat(resized).st_size)
