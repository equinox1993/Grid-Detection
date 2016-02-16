__author__ = 'Edwin'

import cv2
import numpy as np
import algorithms as imalg

def crop_cell(img, tl, tr, bl, br):
    xs = [tl[0], tr[0], bl[0], br[0]]
    ys = [tl[1], tr[1], bl[1], br[1]]
    left = min(xs)
    right = max(xs)
    top = min(ys)
    bot = max(ys)

    cropped = img[top:bot, left:right]

    return np.copy(cropped)

    # mask other
    # shape = bot - top, right - left
    # mask = np.zeros(shape=shape)
    # shifted = np.array([
    #     [tl[0] - left, tl[1] - top],
    #     [tr[0] - left, tr[1] - top],
    #     [br[0] - left, br[1] - top],
    #     [bl[0] - left, bl[1] - top],
    # ])
    # cv2.fillConvexPoly(mask, shifted, 255)

    # return cv2.bitwise_and(cropped, cropped, mask=mask)


def split_grid(img, v_mat):
    mat = []

    def slide_fn(tl, tr, bl, br, isn):
        if isn:
            row = []
            mat.append(row)
        else:
            row = mat[len(mat) - 1]
        cropped = crop_cell(img, tl, tr, bl, br)
        row.append(cropped)
    imalg.slide_vertex_mat_4pts(v_mat, slide_fn)
    return mat