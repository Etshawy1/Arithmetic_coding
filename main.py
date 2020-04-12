#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 04:08:19 2020

@author: etshawy
"""

import cv2
import numpy as np

img = cv2.imread("baboon.bmp")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
block_size = 8


data = np.array(img)
flattened = data.flatten()
probabilities = np.zeros(256, np.float64)

# calculate probabilites
for pixel in flattened:
    probabilities[pixel] += 1
probabilities /= len(flattened)

# eliminate zero probabilities
prob_keys = []
prob_values = []
for i in range(256):
    if probabilities[i] != 0:
        prob_keys.append(i)
        prob_values.append(probabilities[i])

# dividing the flattened photo into blocks      

blocks = np.reshape(flattened, (int(len(flattened)/block_size), block_size))     

 

# encoding each block
sum_previous_symbols_probs = np.cumsum(prob_values)

codes = np.zeros(len(blocks), np.float64)

for i in range(len(blocks)):
    lower_bound = 0
    upper_bound = 1
    for symbol in blocks[i]:
        current_symbol_index = prob_keys.index(symbol)
        current_range = upper_bound - lower_bound
        upper_bound = lower_bound + (current_range * sum_previous_symbols_probs[current_symbol_index])
        if current_symbol_index != 0: 
            lower_bound = lower_bound + (current_range * sum_previous_symbols_probs[current_symbol_index - 1])
        else:
            lower_bound = lower_bound
    codes[i] = (lower_bound + upper_bound) / 2


np.save('image.npy', codes)

decoded_blocks = np.zeros((int(len(flattened)/block_size), block_size)) 
# decoding
for i in range(len(codes)):
    for j in range(block_size):
        upper_bound_index = np.argmax(sum_previous_symbols_probs > codes[i])
        upper_bound = sum_previous_symbols_probs[upper_bound_index]
        if upper_bound_index != 0:
            lower_bound_index = upper_bound_index - 1
            lower_bound = sum_previous_symbols_probs[lower_bound_index]
        else:
            lower_bound = 0
        decoded_blocks[i,j] = (prob_keys[upper_bound_index])
        current_range = upper_bound - lower_bound
        codes[i] = (codes[i] - lower_bound) / current_range


decoded_img = np.reshape(decoded_blocks, (256, 256)) 
decoded_img = decoded_img.astype(np.uint8)

cv2.imshow('Gray image', decoded_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

    
    