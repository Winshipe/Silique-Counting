# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 17:59:26 2016

@author: Eamon
"""
#import sys
from tracing_stems import *
def main():
    name = "C:/Users/Eamon/Documents/ShiuLab/finding siliques by difference/testing/1-1_r.png"#sys.argv[1]
    img = open_im(name)
#    bw = img.convert('L')
    bw = threshold(img)
#    bw.save("C:/Users/Eamon/Documents/ShiuLab/finding siliques by difference/testing/thresholded_1-1.jpg")
    npa = np.array(bw)
#    coms = find_centers_of_mass(npa)
    coords = find_start_point(npa)
    npa2 = eliminate_main_stem(coords,npa)
    img2 = im.fromarray(npa2)    
#    img2.show()
    img2.save("C:/Users/Eamon/Documents/ShiuLab/finding siliques by difference/testing/stem_subtracted_norm.jpg")
main()