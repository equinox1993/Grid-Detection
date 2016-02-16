__author__ = 'Edwin'

import cv2

BINARIZATION_WHITE = 255


def canny(gray, threshold1, threshold2):
    return cv2.Canny(gray,threshold1, threshold2)


def threshold(gray, threshold):
    th, binary = cv2.threshold(gray, threshold, BINARIZATION_WHITE, cv2.THRESH_BINARY_INV)
    return binary


def adaptive_threshold(gray, block_size, c=1):
    return cv2.adaptiveThreshold(gray, BINARIZATION_WHITE,
                                 cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, c)