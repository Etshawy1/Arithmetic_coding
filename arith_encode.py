#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 21:03:05 2020

@author: etshawy
"""
import cv2
import numpy as np
from fractions import Fraction

def encode(img, block_size, data_type):
    
    print('encoding...')
    
    # read and flatten the image 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    data = np.array(img)
    flattened = data.flatten()
    
    # make 1d np array for the probabilities
    f10 = np.zeros(256)
    if data_type != 'f16':
        probabilities = np.array([Fraction(d) for d in f10])
    else:
        probabilities = np.zeros(256, dtype = 'f16')
    
    # calculate probabilites
    for pixel in flattened:
        probabilities[pixel] += 1
    probabilities /= len(flattened)
    
    pp = np.array(probabilities, copy = True)
    
    # lower_bound is c, upper_bound is d, they hold cumulative probabilites
    c = []
    d = []
    c.append(0)
    
    # eliminate zero probabilities and calculate upper and lower bounds
    prob_keys = []
    for i in range(256):
        if probabilities[i] != 0:
            prob_keys.append(i)
            d.append(c[-1] + probabilities[i])
            c.append(d[-1])
    c.pop()
          
    # padding flattened data and dividing the flattened photo into blocks      
    while len(flattened) % block_size != 0:
        flattened = np.append(flattened, 0)
    blocks = np.reshape(flattened, (int(len(flattened)/block_size), block_size))     
    
    
    codes = np.zeros(len(blocks), dtype = data_type)
    
    # calculate the code for every block
    for i in range(len(blocks)):
        lower_bound = 0
        upper_bound = 1
        for symbol in blocks[i]:
            if not symbol in prob_keys:
                continue
            current_symbol_index = prob_keys.index(symbol)
            current_range = upper_bound - lower_bound
            upper_bound = lower_bound + (current_range * d[current_symbol_index]) 
            lower_bound = lower_bound + (current_range * c[current_symbol_index])
        codes[i] = (lower_bound + upper_bound) / 2
    
    # save the binary data for the codes
    np.save('image.npy', codes)
    
    # return the probabilites to be used by the decoder
    return pp
