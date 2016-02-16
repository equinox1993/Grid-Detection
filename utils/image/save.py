__author__ = 'Edwin'

import cv2


def get_default_filename_func(prefix):
    return lambda i, j: prefix + '/cell_' + repr(i) + "_" + repr(j) + ".jpg"


# filename_fn(grid-i, grid-j)->string
def save_cropped_image_grids(grid, filename_fn):
    for i in range(0, len(grid)):
        row = grid[i]
        for j in range(0, len(row)):
            filename = filename_fn(i, j)
            img = grid[i][j]
            cv2.imwrite(filename, img)