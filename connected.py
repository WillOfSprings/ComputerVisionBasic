import imageio.v2 as iio
import cv2

image = cv2.imread('./images/image.png') #reading the image using opencv
image = image[...,::-1] #converting defualt BGR to RGB by taking the reverse -> image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB) #library function for the same 
red = image[:,:,0] 
blue = image[:,:,1]
green = image[:,:,2]
gray = red*0.33+blue*0.33+green*0.33 
binary = gray.copy()
(row,col) = gray.shape[0:2]
for i in range(row):
    for j in range(col):
        if(gray[i,j]>128):
            binary[i,j] = 1
        else:
            binary[i,j] = 0
iio.imwrite("./images/binary.png",binary)
components = 0
#connected components code ------------------------------------------------------
component_matrix = [[0 for i in range(col)] for j in range(row)]
mapper = {}

if (binary[0][0] == 1):
    components= components+1
    mapper[components] = components
    component_matrix[0][0] = components

#for 0th row
for r in range(row):
    if(r>0):
        if(component_matrix[r-1][0]!=0 and component_matrix[r-1][1]==0 and binary[r][0] == 1):
            component_matrix[r][0] = component_matrix[r-1][0]
        elif(component_matrix[r-1][0]==0 and component_matrix[r-1][1]!=0 and binary[r][0] == 1):
            component_matrix[r][0] = component_matrix[r-1][1]
        elif(component_matrix[r-1][0]!=0 and component_matrix[r-1][1]!=0 and binary[r][0] == 1):
            if(component_matrix[r-1][0]<=component_matrix[r-1][1]):
                component_matrix[r][0] = component_matrix[r-1][0]
                mapper[component_matrix[r-1][1]] = mapper[component_matrix[r-1][0]]
            else:
                component_matrix[r][0] = component_matrix[r-1][1]
                mapper[component_matrix[r-1][0]] = mapper[component_matrix[r-1][1]]
        elif(binary[r][0] == 1):
            components= components+1
            mapper[components] = components
            component_matrix[r][0] = components

for r in range(row):
    if(r>0):
        if(binary[r][col-1] == 1):
            if( component_matrix[r-1][col-1]==0 and component_matrix[r][col-1-1]==0 and component_matrix[r-1][col-1-1]==0 ):
                components= components+1
                mapper[components] = components
                component_matrix[r][col-1] = components
            elif( component_matrix[r-1][col-1]!=0 and component_matrix[r][col-1-1]==0 and component_matrix[r-1][col-1-1]==0 ):
                component_matrix[r][col-1] = component_matrix[r-1][col-1]
            elif(component_matrix[r-1][col-1]==0 and component_matrix[r][col-1-1]!=0 and component_matrix[r-1][col-1-1]==0 ):
                component_matrix[r][col-1] = component_matrix[r][col-1-1]
            elif(component_matrix[r][col-1]==0 and component_matrix[r][col-1-1]==0 and component_matrix[r-1][col-1-1]!=0 ):
                component_matrix[r][col-1] = component_matrix[r-1][col-1-1]
            else:
                list = [component_matrix[i][j-1],component_matrix[i-1][j], component_matrix[i-1][j-1]]
                for val in list:
                    if (val == 0):
                        list.remove(val)
                minimum = min(list)
                if(minimum!=0):
                    component_matrix[i][j] = minimum
                for val2 in list:
                    if(minimum!=0):
                        mapper[val2] = mapper[mapper[minimum]] 


#for 0th column
for c in range(col):
    if(c>0):
        if(component_matrix[0][c-1]!=0 and binary[0][c] == 1):
            component_matrix[0][c] = component_matrix[0][c-1]
        elif(binary[0][c] == 1):
            components= components+1
            mapper[components] = components
            component_matrix[0][c] = components

#nested loop for all pixels to find components
for i in range(1,row):
    for j in range(1,col):
         if(binary[i][j] == 1 and j+1<col):
            if( component_matrix[i-1][j]==0 and component_matrix[i][j-1]==0 and component_matrix[i-1][j-1]==0 and component_matrix[i-1][j+1]==0):
                components= components+1
                mapper[components] = components
                component_matrix[i][j] = components
            elif( component_matrix[i-1][j]!=0 and component_matrix[i][j-1]==0 and component_matrix[i-1][j-1]==0 and component_matrix[i-1][j+1]==0):
                component_matrix[i][j] = component_matrix[i-1][j]
            elif(component_matrix[i-1][j]==0 and component_matrix[i][j-1]!=0 and component_matrix[i-1][j-1]==0 and component_matrix[i-1][j+1]==0):
                component_matrix[i][j] = component_matrix[i][j-1]
            elif(component_matrix[i-1][j]==0 and component_matrix[i][j-1]==0 and component_matrix[i-1][j-1]!=0 and component_matrix[i-1][j+1]==0):
                component_matrix[i][j] = component_matrix[i-1][j-1]
            elif(component_matrix[i-1][j]==0 and component_matrix[i][j-1]==0 and component_matrix[i-1][j-1]==0 and component_matrix[i-1][j+1]!=0):
                component_matrix[i][j] = component_matrix[i-1][j+1]
            else:
                list = [component_matrix[i][j-1],component_matrix[i-1][j], component_matrix[i-1][j-1], component_matrix[i-1][j+1]]
                for val in list:
                    if (val == 0):
                        list.remove(val)
                minimum = min(list)
                if(minimum!=0):
                    component_matrix[i][j] = minimum
                for val2 in list:
                    if(minimum!=0):
                        mapper[val2] = mapper[mapper[minimum]] 

#reputting all unique connected componenets
for key in mapper:
    mapper[key] = mapper[mapper[key]]

for q in range(row):
    for s in range(col):
        if(component_matrix[q][s]!=0):
            component_matrix[q][s] = mapper[component_matrix[q][s]]


list = []
#calculating number of connected components from map
for key in mapper:
    if(mapper[key] not in list):
        list.append(mapper[key])
#print(mapper)
print("No. of Connected Components = ",len(list))

#print(component_matrix)