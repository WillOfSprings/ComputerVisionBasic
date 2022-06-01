import random
import xlsxwriter
import numpy as np
workbook = xlsxwriter.Workbook('hello.xlsx')

sheet1 = workbook.add_worksheet()

sheet1.write('A1','a')
sheet1.write('B1','b')
sheet1.write('C1','op')
sheet1.write('D1','c')
sheet1.write('E1','d')
sheet1.write('F1','real')
sheet1.write('G1','imaginary')
counter = 2
for i in range(0,100000):
    a = random.randrange(1, 100, 1)
    b = random.randrange(1, 100, 1)
    c = random.randrange(1, 100, 1)
    d = random.randrange(1, 100, 1)
    #operator = random.randrange(0, 4, 1)
    if(i<=37500):
        operator = 3
    elif(i<=75000):
        operator = 2
    elif(i<=87500):
        operator = 1
    else:
        operator = 0

    real = 0
    imaginary = 0
    flag = 0
    if(operator==0):
        real = a+c
        imaginary = b+d
        flag =1
    if(operator==1):
        real = a-c
        imaginary = b-d
        if(real>=0 and imaginary>=0):
            flag = 1
    if(operator==2):
        real = a*c - b*d
        imaginary = a*d + b*c
        if(real>=0 and imaginary>=0):
            flag = 1
    if(operator==3 and (c!=0 or d!=0)):
        real = (a*c + b*d) / (c*c + d*d)
        imaginary = (b*c - a*d) / (c*c + d*d)
        if(real>=0 and imaginary>=0):
            flag = 1
    if(flag == 1):
        sheet1.write("A"+str(counter),a)
        sheet1.write("B"+str(counter),b)
        sheet1.write("C"+str(counter),operator)
        sheet1.write("D"+str(counter),c)
        sheet1.write("E"+str(counter),d)
        sheet1.write("F"+str(counter),real)
        sheet1.write("G"+str(counter),imaginary)
        counter = counter+1

workbook.close()