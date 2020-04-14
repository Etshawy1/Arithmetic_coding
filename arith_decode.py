#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 23:02:39 2020

@author: etshawy
"""
import bisect
import numpy as np
import cv2
from math import ceil


def decode(height, width, block_size, probabilities):

    print('decoding...')

    # load binary data
    codes = np.load('image.npy')

    decoded_blocks = np.zeros((ceil(height * width / block_size), block_size))

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

    # decode the code that represent each block data
    for i in range(len(codes)):
        for j in range(block_size):
            upper_bound_index = bisect.bisect_left(d, codes[i])
            upper_bound = d[upper_bound_index]
            lower_bound = c[upper_bound_index]
            decoded_blocks[i, j] = (prob_keys[upper_bound_index])
            current_range = upper_bound - lower_bound
            codes[i] = (codes[i] - float(lower_bound)) / float(current_range)
            if codes[i] > 1:
                codes[i] = 1

    # flatten the decoded blocks to remove any padding done at the last block
    flattened = decoded_blocks.flatten()
    to_remove = len(flattened) % (height * width)
    if to_remove:
        flattened = flattened[:-to_remove]

    # turn the flat decoded blocks into an image providing its width and height
    decoded_img = np.reshape(flattened, (height, width))
    decoded_img = decoded_img.astype(np.uint8)

    print('photo decoded successfully press any key on the open photo window to terminate the program')
    # show the decoded image and store it as output.png
    cv2.imshow('Gray image', decoded_img)
    cv2.imwrite('output.png', decoded_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
