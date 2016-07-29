# -*- coding: utf-8 -*-
"""
Created on Thu May 12 13:53:37 2016

@author: Eamon
"""

from PIL import Image as im
from PIL import ImageOps as imo
#from PIL import ImageChops as imc
import os
from scipy import ndimage
from scipy import stats as st
import numpy as np
import gc
#import sys
import math
#import timeit
def open_image(path,filename):
    os.chdir(path)
    try:
        img = im.open(filename)
    except FileNotFoundError:
        img = None
    except IOError:
        img = None
    return img
def convert_to_gs(img):
    '''converts image to grey scale and thresholds st any pixel <50 is made black'''
    bw = img.convert('L')
    bw = imo.invert(bw)
    bw = bw.point(lambda x:0 if x<75 else x)
    return bw
def find_centers(npa):
    '''returns list of brightest points ie stalk'''
    pointsx = list()
    pointsy = list()
#    print(npa.ndim)
    for i in range(int(npa.shape[0]/4),int(npa.shape[0]),5):
        pointx = ndimage.measurements.center_of_mass(npa[i,0:])[0]
        pointsx.append(pointx)
    for j in range(int(npa.shape[1]/4),int(npa.shape[1]),5):
        pointy = ndimage.measurements.center_of_mass(npa[0:,j])[0]        
        pointsy.append(pointy)
    pointsx.reverse()
    pointsy.reverse()
    return pointsx,pointsy
def find_angles(points1,points2,offset,ny):
    '''returns median angle b/w stalks'''
    angles = list()
    length = min((len(points1),len(points2)))
    for i in range(length):
        dist = abs(points1[i]-points2[i]+offset)
        angle = math.degrees(math.atan(dist/ny))
        angles.append(angle)
        if i<10:
            angles.append(angle)###weights bottom of stem higher
    med_angle = np.median(angles)
    return med_angle
def find_offset(points1,points2):
    lens = [len(points1),len(points2)]
    m = min(lens)
#    print(m,lens)
    diffs = list()
    for j in range(m):
        diff = points1[j]-points2[j]
        diffs.append(diff)
    mode = round(float(st.mode(diffs)[0]),0)
    offset = int(mode)
    return offset
def optimize_offset(npa,npa2):
    count = 0
    diff = 100
    oldy = 0
    oldx = 0
    POINTSX,POINTSY = find_centers(npa)
    while diff>1 and count>99:
        pointsx2,pointsy2 = find_centers(npa2)
        offx = find_offset(POINTSX,pointsx2)
        offy = find_offset(POINTSY,pointsy2)
        diff = (offx-oldx)+(offy-oldy)
        npa2 = np.roll(npa2,offx,0)
        npa2 = np.roll(npa2,offy,1)
        count+=1
        oldy = offy
        oldx = offx
    print(count)
    return npa2
def adjust_and_subtract_imgs(img1,img2):
    npa = np.array(img1)
    npa2 = np.array(img2)
    pointsx,pointsy = find_centers(npa)
    pointsx2,pointsy2 = find_centers(npa2)
    init_offset = find_offset(pointsx,pointsx2)
    angle = find_angles(pointsx,pointsx2,init_offset,npa.shape[1])
    npa2 = ndimage.interpolation.rotate(npa2,angle)
    npa2 = optimize_offset(npa,npa2)
    remainder = np.subtract(npa,npa2)
    img = im.fromarray(remainder)
    return img
#def resize_and_center_plant(img,img2):
#    '''centers and overlaps plants'''
#### crops the image to just the plant (hopefully!) ###
#    bw = convert_to_gs(img)
#    bw2 = convert_to_gs(img2)
#    box = bw.getbbox()
#    bw = bw.crop(box)
##    imo.expand(bw,border=300,fill="white").show()
#    box2 = bw2.getbbox()
#    bw2 = bw2.crop(box2)
##    imo.expand(bw2,border=300,fill="white").show()
#    npa = np.array(bw)
#    npa2 = np.array(bw2)
##    print(ndimage.measurements.center_of_mass(npa))
##    print(ndimage.measurements.center_of_mass(npa2))
#### Adjust st the stalks overlap ###
#    
#    bw_size = (len(np.invert(npa)[0,0:]),len(npa[0,0:]))
#    bw2_size = (len(np.invert(npa2)[0,0:]),len(npa2[0,0:]))
#    ny = max((bw_size[1],bw2_size[1]))+offsety
##        angle = int(round(find_angles(points1,points2,offset,ny),0))
#    npa2 = ndimage.interpolation.rotate(npa2,angle)
#     
#    
#    
#    nx = max((bw_size[0],bw2_size[0]))+offsetx ### leaves room for the whole plant in final image 
#    nimg = im.new("RGB",(nx,ny),'blue') ### creates new images that are the same size st the plants can overlap
#    nimg2 = im.new("RGB",(nx,ny),'blue')
#    print(bw_size,bw2_size,offsetx,offsety)
##    height = (bw.size[1]-bw2.size[1]) if (bw.size[1]>bw2.size[1]) else (bw2.size[1]-bw.size[1])
##    if stalk_x>stalk_x2:
#    nimg.paste(bw2,(0,offsety+ny-bw2_size[1])) ### moves the plant over  bw2.rotate(angle),
##        nimg.show()
#    nimg2.paste(bw,(0,ny-bw_size[1]))
##        nimg2.show()
#    bw.close()
#    bw.close()
#    return nimg2,nimg
##    else:
##        nimg.paste(bw,(offset,ny-bw.size[1]))
###        nimg.show()
##        nimg2.paste(bw2.rotate(angle),(0,ny-bw2.size[1]))
###        nimg2.show()
##        return nimg,nimg2
###    if box>box2:
###        img2 = img2.resize(img.size,im.ANTIALIAS)
###    else:
###        img = img.resize(img2.size,im.ANTIALIAS)
#def subtract_and_save(img,img2,path):
#    st = timeit.default_timer()
#    img3 = imc.difference(img,img2)
#    print(timeit.default_timer()-st)
#    img3 = imo.invert(img3)
#    img3.save(path+'processed/'+name1[:-4]+_+name2)
def main():
#    global name1,name2
#    name1, name2 = sys.argv[1],sys.argv[2]
#    name1,name2 = '1-2.jpg',"1-2-.jpg"
#    if not sys.argv[3]:
#        path = "C:/Users/Eamon/Documents/ShiuLab/"
#    else:
#        path = sys.argv[3]
    path = "C:/Users/Eamon/Documents/ShiuLab/finding siliques by difference/testing/"
    try:
        os.mkdir(path+'processed/')
    except WindowsError:
        pass
    files1 = []
    for paths,names,files in os.walk(path):
        for file in files:
            files1.append(file)
    for i in range(0,len(files1),2):
        global name1,name2
        name1,name2 = files1[i],files1[i+1]
        img = open_image(path,name1)
        img2 = open_image(path,name2)
        if img == None or img2 == None:
            continue
        print(files1[i],files1[i+1])
#        img,img2 = resize_and_center_plant(img,img2)
#        subtract_and_save(img,img2,path)
        img.close()
        img2.close()
        gc.collect()
main()