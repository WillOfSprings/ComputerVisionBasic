import imageio as iio
binary = iio.imread('binary.jpg')
(row,col) = binary.shape[0:2]
count = 0
for i in range(row):
    for j in range(col):
        if(binary[i][j] != 255 and binary[i][j]!=0 ):
            print(binary[i][j])