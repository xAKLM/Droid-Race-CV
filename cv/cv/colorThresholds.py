import numpy as np

def blue_limits_HSV():  
    lower_blue = np.array([62,62,119]) #93 100 100
    upper_blue = np.array([130,238,205]) #130 255 255
    return (lower_blue, upper_blue)

def yellow_limits_HSV():
    lower_yellow = np.array([0,0,174])
    higher_yellow = np.array([255, 33, 255])
    return (lower_yellow, higher_yellow)

def purple_limits_HSV():
    lower_purple = np.array([143,100, 100])
    higher_purple = np.array([166, 255, 255])
    return (lower_purple, higher_purple)
