__author__ = 'Edwin'

import cv2
import binarizewolfjolion as wolf

BINARIZATION_WHITE = 255


def canny(gray, threshold1, threshold2):
    return cv2.Canny(gray,threshold1, threshold2)


def threshold(gray, threshold):
    th, binary = cv2.threshold(gray, threshold, BINARIZATION_WHITE, cv2.THRESH_BINARY_INV)
    return binary


def adaptive_threshold(gray, block_size, c=1):
    return cv2.adaptiveThreshold(gray, BINARIZATION_WHITE,
                                 cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size, c)


def binarizewolfjolion(img, winx=0, winy=0, k=0.5, dR=128):
    if winx == 0 or winy == 0:
        winx, winy = _get_default_win_size(img)

    return wolf.binarize(img, winx, winy, k, dR)


def _get_default_win_size(input):
    rows = input.shape[0]
    cols = input.shape[1]
    winy = int((2.0 * rows-1)/3)
    winx = cols-1 if int(cols-1 < winy) else winy
    # if the window is too big, than we assume that the image
    # is not a single text box, but a document page: set
    # the window size to a fixed constant.
    if winx > 100:
        winx = winy = 40
    return winx, winy