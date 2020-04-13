#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 22:50:56 2020

@author: etshawy
"""

def input_block_size(message):
  while True:
    try:
       userInput = int(input(message))       
    except ValueError:
       print("Not an integer! Try again.")
       continue
    else:
       return userInput 
       break 

def input_data_type(message):
  while True:
    i = input(message)
    if i == '1' or i.lower() == 'float16':  
        return 'f2'
        break  
    elif i == '2' or i.lower() == 'float32':  
        return 'f4'
        break
    elif i == '3' or i.lower() == 'float64':  
        return 'f8'
        break
    elif i == '4' or i.lower() == 'float128':  
        return 'f16'
        break
    else: 
        print('please enter a valid data type')
