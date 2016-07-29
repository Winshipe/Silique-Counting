# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 16:47:45 2016

@author: Eamon
"""
#import sys
from PIL import Image as im
from PIL import ImageOps as imo
#from PIL import ImageDraw as imd
from scipy import ndimage
from scipy import stats as st
import numpy as np
import math
import copy
#import find_siliques_by_difference_preprocessing2 as fs
def open_im(name):
    print("opening")
    try:
        img = im.open(name)
    except FileNotFoundError:
        img = None
    return img
def threshold(img):
    print("thresholding")
    bw = img.convert('L')
    bw = imo.invert(bw)
    bw2 = bw.point(lambda x:0 if x<135 else x)
#    bw2.show()
    return bw2
def find_start_point(npa):
    print('finding start point')
#    print(npa.shape)
    len_y = npa.shape[1]-1
    j = int()
    prev = 0
    row = []
    for i in range(len_y,int(0.8*float(len_y)),-1): 
        row = npa[i,0:]
        if i<len_y:
            prev = npa[i+1,0:]
        if len(row[row>130]) and len(prev[prev>130]):
            j = i
            break
    try:
        st_pt = ndimage.center_of_mass(row)[0]
    except RuntimeWarning:
        print(row[row>130])
#    print(j,st_pt)
    try:
        pts = ndimage.measurements.center_of_mass(npa[0:int(npa.shape[1]*0.6),0:])
    except RuntimeWarning:
        print(npa[0:int(npa.shape[1]*0.6),0:])
#    print(pts)
### Testing ###
#    img = im.fromarray(npa)
#    img.convert('RGB')
#    draw = imd.Draw(img)
#    draw.ellipse((pts[1]-20,pts[0]-20,pts[1]+20,pts[0]+20),fill="red")
#    
#    img.show()
#    del draw
################
    cm_x = int(pts[1])
    return (st_pt,j,cm_x)    
def find_centers_of_mass(arr):
    print('finding centers')
#    bw = im.fromarray(arr)
#    img = bw.convert("RGB")
    coms = dict()
    for i in range(0,arr.shape[0],200):
        com = 0
        reg = arr[i:i+200,:]
        if not len(reg[reg>0]):
            continue
        com = ndimage.measurements.center_of_mass(reg)[1]
        coms[i] = com
### TESTING ###
#        draw = imd.Draw(img)
#        draw.ellipse((com-5,i+45,com+5,i+55),fill="red")
#        draw.line([(0,i),(arr.shape[1],i)],fill="red")

#        print(com,i)
#    img.show()
#    img.save("C:/Users/Eamon/Documents/ShiuLab/finding siliques by difference/centers_of_mass_every_100.jpg")
#    del draw
#################
    return coms
#def pdf_stems(arr):
##    positions=[]
##    if type(x)==type(np.array([])):
##        while len(x[x>211]):
##            pos = np.argmax(x>211)
##            positions.append(pos)
##            x[pos]=0
#    out =[]
#    try:
#        for x in arr:
#            x=int(x)
#            y = (3.69529243461e-38*x**19+-4.48698990132e-35*x**18+1.89099078491e-32*x**17+-2.14064885368e-30*x**16+-5.32988469672e-28*x**15+8.104541612e-26*x**14+2.45434944068e-23*x**13+-1.62918982877e-21*x**12+-1.14858107431e-18*x**11+-3.28528818466e-17*x**10+4.57483546992e-14*x**9+5.0296959792e-12*x**8+-1.63630552521e-09*x**7+-2.84903884938e-07*x**6+6.83604564076e-05*x**5+0.00963754566612*x**4+-4.0723137475*x**3+495.351249286*x**2+-27803.6640549*x**1+618184.621393*x**0)
#            if x>211 or y<0:
#                y=0
#            out.append(y)
#    except TypeError:
#        x=arr
#        x=int(x)
#        y = (3.69529243461e-38*x**19+-4.48698990132e-35*x**18+1.89099078491e-32*x**17+-2.14064885368e-30*x**16+-5.32988469672e-28*x**15+8.104541612e-26*x**14+2.45434944068e-23*x**13+-1.62918982877e-21*x**12+-1.14858107431e-18*x**11+-3.28528818466e-17*x**10+4.57483546992e-14*x**9+5.0296959792e-12*x**8+-1.63630552521e-09*x**7+-2.84903884938e-07*x**6+6.83604564076e-05*x**5+0.00963754566612*x**4+-4.0723137475*x**3+495.351249286*x**2+-27803.6640549*x**1+618184.621393*x**0)
#        if x>211 or y<0:
#            y=0
#        out.append(y)
#    out = np.array(out)
#    return out
##    if type(y) == type(np.array([])):
##        y[y<0] = 0
##        y[y>1] = 0
##    elif y<0:
##        y = 0
##    elif x>211:
##        y = 0
##    return y
#def pdf_branches(arr):
#    if type(arr) != type(np.array([])):
#        arr = np.array(arr)
##    print(arr)
#    out = []
#    try:
#        for x in arr:
#            x=int(x)
#            y = (-6.13670842624e-22*x**13+7.08603725781e-19*x**12+-3.19469506389e-16*x**11+6.22942046999e-14*x**10+-9.39975548908e-13*x**9+-1.52559340971e-09*x**8+1.11623097019e-07*x**7+3.69995500189e-05*x**6+-0.00509613745313*x**5+-0.70268725896*x**4+236.323336385*x**3+-25312.9709429*x**2+1287367.87862*x**1+-26350993.9711*x**0)
#            if x>177 or y<0:
#                y=0
#            out.append(y)
#    except TypeError:
#        x=arr
#        x=int(x)
#        y = (-6.13670842624e-22*x**13+7.08603725781e-19*x**12+-3.19469506389e-16*x**11+6.22942046999e-14*x**10+-9.39975548908e-13*x**9+-1.52559340971e-09*x**8+1.11623097019e-07*x**7+3.69995500189e-05*x**6+-0.00509613745313*x**5+-0.70268725896*x**4+236.323336385*x**3+-25312.9709429*x**2+1287367.87862*x**1+-26350993.9711*x**0)
#        if x>177 or y<0:
#            y=0
#        out.append(y)
#    out = np.array(out)
#    return out
#def pdf_siliques(arr):
##    positions=[]
##    if type(x)==type(np.array([])):
##        while len(x[x>215]):
##            pos = np.argmax(x>215)
##            positions.append(pos)
##            x[pos]=0
#    if type(arr) != type(np.array([])):
#        arr = np.array(arr)
#    out = []
#    try:
#        for x in arr:
#            x = int(x)
#            y = (9.96135795844e-17*x**10+-1.67143673354e-13*x**9+1.25639037651e-10*x**8+-5.57067197354e-08*x**7+1.61320075819e-05*x**6+-0.00318765732859*x**5+0.435186509917*x**4+-40.5248522622*x**3+2462.87475534*x**2+-88190.184362*x**1+1412515.29574*x**0)
#            if x>215 or y<0:
#                y=0
#            out.append(y)
#    except TypeError:
#        x=arr
#        x=int(x)
#        y = (9.96135795844e-17*x**10+-1.67143673354e-13*x**9+1.25639037651e-10*x**8+-5.57067197354e-08*x**7+1.61320075819e-05*x**6+-0.00318765732859*x**5+0.435186509917*x**4+-40.5248522622*x**3+2462.87475534*x**2+-88190.184362*x**1+1412515.29574*x**0)
#        if x>215 or y<0:
#            y=0
#        out.append(y)
#    out = np.array(out)
##    if type(y) == type(np.array([])):
##        y[y<0] = 0
##        y[positions]=0
##    elif y<0:
##        y = 0
##    elif x>215:
##        y = 0
#    return out
def branches(x):
    return -3.23966352369e-05*x**7+-0.000559509654358*x**6+0.0015605603416*x**5+0.0518931964765*x**4+0.0104060713501*x**3+-1.69492248126*x**2+-0.487188436367*x**1+163.581815546*x**0
def stem(x):
    return -0.000422099507819*x**5+0.0077688613631*x**4+-0.0251525999156*x**3+-1.74088713628*x**2+1.25577764276*x**1+198.826313489*x**0 
def siliques(x):
    return -2.50753087605e-06*x**6+5.49333185714e-06*x**5+0.00191005064377*x**4+-0.00370982045403*x**3+-0.442515231452*x**2+0.665437312291*x**1+188.421853128*x**0
def best_fit(row,test=False):
    '''Finds the least sum of squares(residual) for branch,stem,silique models.  Returns True if branch or stem fit better than silique'''
    cent = int(round(len(row)/2.0,2))
    pos = [i-cent for i in range(len(row))]
    b_res = np.sqrt(sum([(branches(pos[i])-row[i])**2 for i in range(len(row))]))
    s_res = np.sqrt(sum([(stem(pos[i])-row[i])**2 for i in range(len(row))]))
    si_res = np.sqrt(sum([(siliques(pos[i])-row[i])**2 for i in range(len(row))]))
    truth = False
    if test:
        print(b_res,s_res,si_res)
    if b_res<si_res or s_res<si_res:
        truth = True
    return truth
def eliminate_main_stem(coords,npa):
    print('eliminating stems')
#    bounds = [coords[2]-500,coords[2]+500]
    count = 0
    cent = coords[2]
    cent1 = coords[2]
#    img2 = im.fromarray(npa)
#    arr = np.array(img2.convert('rgb'))
    arr = copy.copy(npa)
    for i in range(coords[1],1,-1):
        row = npa[i,0:]
#        if count==0:
#            count+=1
#            print(type(row))
#            print(len(row))
#            print(row.shape) 
#            print(row.size)
        lbounds = []
        rbounds=[]
        for j in range(len(row)):
            try:
#                if row[j]>0 and not i%100:
#                    print(row[j-1],row[j],row[j+1])
                if row[j-1]<130 and row[j]>130:
                    lbounds.append(j)
                elif row[j]>130 and row[j+1]<130:
                    rbounds.append(j)
            except IndexError:
                continue
#        if not i%100:
#            print(lbounds,rbounds)
#        stem = None
        if (len(lbounds)+len(rbounds))==2:
            row[lbounds[0]:rbounds[0]]=0
            cent = (lbounds[0]+rbounds[0])/2
            continue
        for k in range(min(len(lbounds),len(rbounds))):
#            p = 0
            f = best_fit(row[lbounds[k]:rbounds[k]])
            w = abs(rbounds[k]-lbounds[k])<=11
            d = (abs(lbounds[k]-cent)<10 or (rbounds[k]-cent)<10)
#            arr[i,arr.shape[1]/2-3:arr.shape[1]+3] = 255
#            else:
#                arr[i,lbounds[k]:rbounds[k]] = 60
            cent1 = (lbounds[k]+rbounds[k])/2
            if d:
                arr[i,lbounds[k]:rbounds[k]] = 60
            if i%2 and abs(cent-cent1)<abs(lbounds[k]-rbounds[k])/3:
                cent = cent1
            if d and w: 
                npa[i,lbounds[k]:rbounds[k]]=20
#                stem = True
        arr[i,cent-5:cent+5] = 255
#            elif not i%10:
#                print(best_fit(row[lbounds[k]:rbounds[k]]),abs(rbounds[k]-lbounds[k])<=15,abs(lbounds[k]-cent)<25 or (rbounds[k]-cent)<25)
#        if not stem and not i%100 and len(row[row>0]):
#            print(i,p)
#            print(lbounds,rbounds)
    img2 = im.fromarray(arr)
    img2.save("C:/Users/Eamon/Documents/ShiuLab/finding siliques by difference/testing/cent_line_tf.jpg")
    print(count)
    print("done")
    return npa
