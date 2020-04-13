#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 04:08:19 2020
@author: etshawy
"""

import user_input
import arith_encode
import arith_decode
import cv2
import bisect
import numpy as np
from fractions import Fraction

path = input('please enter the absolute path to the image: ')
block_size = user_input.input_block_size('please enter the block size: ')
data_type = user_input.input_data_type("""please choose one of the following types
    1-float16
    2-float32
    3-float64
    4-float128
    """)

img = cv2.imread(path)
height, width, channels = img.shape

probabilities = arith_encode.encode(img, block_size, data_type)
arith_decode.decode(height, width, block_size, probabilities)


