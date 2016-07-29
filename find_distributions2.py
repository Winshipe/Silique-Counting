# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 13:53:19 2016

@author: Eamon

Looks at distributions of intensities by position 
"""

import tracing_stems as ts
import numpy as np
from scipy import stats as st
import matplotlib.pyplot as plot
#import random
def isolate_branches(arr):
    branch_region = arr[691:753,1358:1396]
    branch_region2 = arr[1171:1201,1401:1451]
    branch_region3 = arr[1297:1297+47,1327:1327+48]
    combined_rows = []
    cr = []
#    rows = []
    for i in range(branch_region.shape[0]):
        row = branch_region[i,:]
#        rows.append(list(row[row>130]))
        combined_rows+=list(row[row>130])
        cr.append(row[row>130])
    for i in range(branch_region2.shape[0]):
        row = branch_region2[i,:]
#        rows.append(list(row[row>130]))
        combined_rows+=list(row[row>130])
        cr.append(row[row>130])
    for i in range(branch_region3.shape[0]):
        row = branch_region3[i,:]
#        rows.append(list(row[row>130]))
        cr.append(row[row>130])
        combined_rows+=list(row[row>130])
    return combined_rows,cr
def isolate_stem(arr):
    stem_region = arr[2153:2153+150,1216:1216+115]
    stem_region2 = arr[503:503+93,1428:1428+24]
    combined_row= []
    cr = []
    for i in range(stem_region.shape[0]):
        row = stem_region[i,:]
#        rows.append(list(row[row>130]))
        combined_row+=list(row[row>130])
        cr.append(row[row>130])
    for i in range(stem_region2.shape[0]):
        row = stem_region2[i,:]
#        rows.append(list(row[row>130]))
        combined_row+=list(row[row>130])
        cr.append(row[row>130])
    return combined_row,cr
def isolate_siliques(arr):
    sil_region = arr[476:476+284,1168:1168+180]
    sil_region2 = arr[820:820+228,1196:1196+160]
    sil_region3 = arr[944:944+240,1444:1444+164]
    sil_region4 = arr[308:308+248,1516:1516+124]
    combined_row= []
    cr = []
    for i in range(sil_region.shape[0]):
        row = sil_region[i,:]
#        rows.append(list(row[row>130]))
        combined_row+=list(row[row>130])
        cr.append(row[row>130])
    for i in range(sil_region2.shape[0]):
        row = sil_region2[i,:]
#        rows.append(list(row[row>130]))
        combined_row+=list(row[row>130])
        cr.append(row[row>130])
    for i in range(sil_region3.shape[0]):
        row = sil_region3[i,:]
#        rows.append(list(row[row>130]))
        combined_row+=list(row[row>130])
        cr.append(row[row>130])
    for i in range(sil_region4.shape[0]):
        row = sil_region4[i,:]
#        rows.append(list(row[row>130]))
        combined_row+=list(row[row>130])
        cr.append(row[row>130])
    return combined_row,cr
def eval_poly(row,coeffs):
    cent = int(round(len(row)/2.0,0))
    fx = [np.polyval(coeffs,i-cent) for i in range(len(row))]
    fx = np.array(fx)
    return fx
def model(rows,num,test=False):
    vals = dict()
    plot.figure(num)
#    r = random.randint(0,len(rows))
    for row in rows:
        cent = int(round(len(row)/2.0,0))
        for i in range(len(row)):
            pos = i-cent
            if pos not in vals:
                vals[pos] = []
            vals[pos].append(row[i])
    for key in vals:
        ints = vals[key]
        val = np.percentile(ints,75)
#        val = int(st.mode(ints)[0])
        vals[key]=val
    coeffs =[]
#    f = 1
    out = ''
    x1=[]
    y1=[]
    for key in sorted(vals.keys()):
        x1.append(key)
        y1.append(vals[key])
    plot.axis([min(x1),max(x1),min(y1),max(y1)])
    plot.plot(x1,y1,'g^')
#    if test:
#        plot.show()
    x1 = np.array(x1)
    y1=np.array(y1)
#    print(x1,y1)
    cols = ['r','g','c','m','y','k']
    s1 = 1e10
    for i in range(0,11):  
        dash = '-' if i<len(cols) else '--'#Used to change line from straight to dashed on matplotlib plot
        col = cols[i%len(cols)]+dash
        coeffs = np.polyfit(x1,y1,i)
        n = ''
        for j in range(len(coeffs)):
            n+=(str(coeffs[j])+'*x**'+str(i-j)+'+')
        n = n[:len(n)-1]
        fx = []
        for i in x1:
            x = i
            fx.append(eval(n))
#        if test:
#            plot.plot(x1,y1,'g^')
        plot.plot(x1,fx,col)
        s = np.sqrt(sum([(y1[i]-fx[i])**2 for i in range(len(fx))]))
        print(s,s1)
        if s<s1:
            dif = abs(s-s1)
            print("T")
            s1=s
            out=n
            if dif<0.5 and s<10:
                break
#        print(rows[r],fx)
#        fp = st.f_oneway(list(vals.values()),fx)
#        if test:
#            print(n)
#            print(i,fp)
#            print('\n')
#        p=fp[1]
##        print(f,f1)
#        if p<0.01:
#            out = n 
#            break
    plot.show()
    plot.close()
#    print(out)
    return out
def avg(comb_row):
#    print(comb_row)
    a = float(sum(list(comb_row)))/float(len(list(comb_row)))
    med = np.median(comb_row)
    mod = st.mode(comb_row)
    print('mean',a,'median',med,'mode',mod)
    print('25%',np.percentile(comb_row,25),'75%',np.percentile(comb_row,75))
#    plot.boxplot(comb_row)
#    plot.show()
#    plot.close()
def create_file(file,comb_row,name):
    out = ''
    for i in comb_row:
        out+=str(i)
        out+=','
        out+=name
        out+='\n'
    file.write(out)
    return file
def main():
#    plot.xkcd()
    name = "C:/Users/Eamon/Documents/ShiuLab/finding siliques by difference/testing/1-1_r.png"
    img = ts.open_im(name)
    bw = ts.threshold(img)
    array = np.array(bw)
    comb_row,cr = isolate_branches(array)
    comb_row2,cr2 = isolate_stem(array)
    comb_row3,cr3 = isolate_siliques(array)
    print("branch")
    avg(comb_row)
    print("stem")
    avg(comb_row2)
    print("silique")
    avg(comb_row3)
    file = open('intensities.txt','w')
    file =create_file(file,comb_row,'branch')
    file =create_file(file,comb_row2,'stem')
    file =create_file(file,comb_row3,'silique')
    file.close()
    n1 = model(cr,1,True)
    plot.close()
    print("stem")
    n2 = model(cr2,2,True)
    plot.close()
    print("siliques")
    n3 = model(cr3,3,True)
    print("branch",n1,'\n\nstem',n2,'\n\nsiliques',n3)
main()
    