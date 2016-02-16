__author__ = 'Edwin'

import cv2
import utils.image.draw_tools as draw
import utils.image.algorithms as imalg
import utils.image.binarization as binz

img = cv2.imread("sample/table1r.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

binary = binz.threshold(gray, 200)
# binary = binz.adaptive_threshold(gray, 171)
# binary = binz.canny(gray, 50, 150)

# cv2.imshow('img', binary)
# cv2.waitKey(0)

# rt_lines = imalg.find_rt_lines(binary, 200)
rt_lines = imalg.find_rt_lines(binary, 350)
two_pts_lines = imalg.rt_lines_to_2pts(rt_lines)
horizontal, vertical = imalg.orthogonal_separation(two_pts_lines)
imalg.sort_2pts_lines(horizontal, 1)
imalg.sort_2pts_lines(vertical, 0)
draw.draw_2pts_lines(img, horizontal, color=(255,0,0))
draw.draw_2pts_lines(img, vertical, color=(0,0,255))
v_mat, vertices = imalg.find_intersection_matrix(horizontal, vertical, thresh=10)
draw.draw_vertex_crosses(img, v_mat)
draw.draw_points(img, vertices)

cv2.imshow('img', img)
cv2.waitKey(0)