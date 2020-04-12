#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 19:43:15 2020

@author: etshawy
"""

# Constants

PRECISION = 32
WHOLE = 2 ** PRECISION
HALF = 2 ** (PRECISION - 1)
QUARTER = 2 ** (PRECISION - 2)


import cv2
import numpy as np

img = cv2.imread("baboon.bmp")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
block_size = 16


data = np.array(img)
flattened = data.flatten()

# number of repititions each symbol
r = np.zeros(256, np.int16)
for pixel in flattened:
    r[pixel] += 1

# lower_bound is c, upper_bound is d
c = []
d = []
c.append(0)
prob_keys = []
for i in range(256):
    if r[i] != 0:
        prob_keys.append(i)
        d.append(c[-1] + r[i])
        c.append(d[-1])
c.pop()       
     
# dividing the flattened photo into blocks      

blocks = np.reshape(flattened, (int(len(flattened)/block_size), block_size))     

#codes = np.zeros((len(blocks), 1), np.bool)
codes = [[0] for i in range(len(blocks))]



for l in range(len(blocks)):
    a = 0
    b = WHOLE
    s = 0
    for symbol in blocks[l]:
        i = prob_keys.index(symbol)
        w = b - a
        b = a + int(round(w * d[i] / len(flattened))) 
        a = a + int(round(w * c[i] / len(flattened)))
        if b < HALF or a > HALF and a != b:
            if b < HALF:
                codes[l].append(0)
                for pad in range(s):
                    codes[l].append(1)
                s = 0
                a = 2 * a
                b = 2 * b
            elif a > HALF:
                codes[l].append(1)
                for pad in range(s):
                    codes[l].append(0)  
                s = 0
                a = 2 * (a - HALF)
                b = 2 * (b - HALF)
        if a > QUARTER and b < 3 * QUARTER:
            a = 2 * (a - QUARTER) 
            b = 2 * (b - QUARTER)
            s = s + 1
    s = s + 1
    if a <= QUARTER:
        codes[l].append(0)
        for pad in range(s):
            codes[l].append(1)
    else:
        codes[l].append(1)
        for pad in range(s):
            codes[l].append(0)

print(codes)
# npcodes = np.packbits(np.array(codes), axis = 1)
print(blocks)
#np.save('image.npy', npcodes)

decoded_blocks = np.zeros((int(len(flattened)/block_size), block_size)) 
# decoding
for q in range(len(codes)):
    a = 0
    b = WHOLE
    z = 0
    i = 1 
    while i <= PRECISION:
        if codes[q][i] == 1:
            z = z + 2 ** (PRECISION - i)
        i+=1
    print(len(codes[q]))
    for symbol in codes[q]:
        for j in range(len(prob_keys)):
            w = b - a
            b0 = a + int(round(w * d[j] / len(flattened))) 
            a0 = a + int(round(w * c[j] / len(flattened)))
            if a0 <= z and z < b0:
                decoded_blocks[q][codes[q].index(symbol)] = (prob_keys[j])
                print(a0)
                print(b0)
                a = a0
                b = b0
        while b < HALF or a > HALF and a != b:
            if b < HALF:
                a = 2 * a
                b = 2 * b
                z = 2 * z
            elif a > HALF:
                z = 2 * (z - HALF)
                a = 2 * (a - HALF)
                b = 2 * (b - HALF)
            if codes[q][i] == 1:
                z = z + 1
                i +=1
        while a > QUARTER and b < 3 * QUARTER:
            a = 2 * (a - QUARTER) 
            b = 2 * (b - QUARTER)
            z = 2 * (z - QUARTER)
            if codes[q][i] == 1:
                z = z + 1
                i +=1
print(decoded_blocks)
decoded_img = np.reshape(decoded_blocks, (256, 256)) 
decoded_img = decoded_img.astype(np.uint8)

cv2.imshow('Gray image', decoded_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

