#-------------------------------------------------------------------------------------#
#Funzione per trasformare una matrice di valori in immagine jpeg
#-------------------------------------------------------------------------------------#

#imports
from PIL import Image
import numpy as np
from PIL import ImageFilter, ImageChops, ImageOps


# Open the image file
with open("C:/Users/giaco/Desktop/trimat_webapp/sensomative/bin/sensomative/Export/Snapshots/2024_03_07/2024_03_07_01.txt") as file: 
    data = file.read()

    data = data[10:-27] #remove first and last row

    #convert the data to a numpy array, data is 16x16
    data = np.array(data.split(), dtype=np.double).reshape(16, 16)
    # make the data bigger for better visualization
    #data = np.kron(data, np.ones((100, 100)))
    #data is a 16x16 matric of pressure values, convert to rgb values for the image
    data = (data - data.min()) / (data.max() - data.min()) * 255
    data = np.stack([data, data, data], axis=2).astype(np.uint8)
    #create an image from the data
    img = Image.fromarray(data)
    #sharp the image
    img = img.filter(ImageFilter.SHARPEN)
    #reshape the image to the correct size
    img = img.resize((1600, 1600))
    #sharp the image
    #img = img.filter(ImageFilter.SHARPEN)


    img.show() #show the image


