from matplotlib import pyplot as plt
import cv2
import imageio as iio
 
 
image = iio.imread('./images/macs.jpg') #reading the image using opencv
#image = image[...,::-1] #converting defualt BGR to RGB by taking the reverse -> image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB) #library function for the same 

plt.title("Coloured")
plt.imshow(image)
plt.show()

# dividing the 3 byte maps
red = image[:,:,0] 
blue = image[:,:,1]
green = image[:,:,2]

#taking the average and dividing individually to avoid overflow
gray = red*0.33+blue*0.33+green*0.33 

plt.title("Grayscale")
plt.imshow(gray, cmap='gray')
plt.show()
iio.imwrite("grayscale.jpg", gray)

#converting into binary
binary = gray.copy()
(row,col) = gray.shape[0:2]
for i in range(row):
    for j in range(col):
        if(gray[i,j]>128):
            binary[i,j] = 1
        else:
            binary[i,j] = 0

plt.title("Binary")
plt.imshow(binary, cmap='gray') #plotting on the assumption 1 is white and 0 is black
plt.show()
iio.imwrite("binary.jpg",binary)
#print(image)
#print(gray)
#print(binary)