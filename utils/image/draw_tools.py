__author__ = 'Edwin'

import cv2

from utils.image import algorithms as imalg


def draw_2pts_lines(img, lines, color=(0, 0, 255), thickness=2):
    for x1, y1, x2, y2 in lines:
        cv2.line(img, (x1,y1), (x2,y2), color, thickness)


def draw_points(img, points, color=(0, 255, 0)):
    for px, py in points:
        cv2.circle(img, (px, py), 2, color, 2)


def draw_vertex_crosses(img, v_mat, color=(255, 0, 255), thickness=2):
    def draw_4pts_cross(tl, tr, bl, br, _):
        cv2.line(img, tl, br, color, thickness)
        cv2.line(img, tr, bl, color, thickness)

    imalg.slide_vertex_mat_4pts(v_mat, draw_4pts_cross)