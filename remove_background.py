import os
from PIL import Image
import numpy as np
from rembg import remove

class preprcessInput:

    def __init__(self):
        self.o_width = None
        self.o_height = None
        self.o_image = None

        self.t_width = None
        self.t_height = None
        self.t_image = None
        self.save_path = None

    def remove_bg(self, file_path: str, save_path: str):
        self.save_path = os.path.join(save_path, os.path.basename(file_path)[:-3] + '.png')
        pic = Image.open(file_path)
        self.o_width = np.asarray(pic).shape[1]
        self.o_height = np.asarray(pic).shape[0]
        try:
            self.o_channels = np.asarray(pic).shape[2]
        except Exception as e:
            print("Single channel image and error", e)
        os.remove(file_path)
        self.o_image = remove(pic)
        self.o_image.save(self.save_path)
        return np.asarray(self.o_image)

    def transform(self, width=768, height=1024):
        newsize = (width, height)
        self.t_height = height
        self.t_width = width

        pic = self.o_image
        img = pic.resize(newsize)

        self.t_image = img

        background = Image.new("RGBA", newsize, (255, 255, 255, 255))
        background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
        self.save_path = os.path.join(self.save_path, os.path.basename(self.save_path)[:-3] + '.jpg')
        background.convert('RGB').save(self.save_path, 'JPEG')

        return np.asarray(background.convert('RGB'))

# USAGE OF THE CLASS
preprocess = preprcessInput()
input_directory = 'imdir'
output_directory = 'imdir_bg'

for image_file in os.listdir(input_directory):
    if image_file.endswith('.jpg'):
        image_path = os.path.join(input_directory, image_file)
        op = preprocess.remove_bg(image_path, output_directory)
        arr = preprocess.transform(768, 1024)
