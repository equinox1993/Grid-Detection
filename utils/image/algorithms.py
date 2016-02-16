__author__ = 'Edwin'

import cv2
import numpy as np


def find_rt_lines(binary, threshold, rho_res = 1, th_res = np.pi/180):
    lines = cv2.HoughLines(binary, rho_res, th_res, threshold)
    return [line[0] for line in lines]


def deduplicate_rt_lines(rt_lines, r_thresh, theta_thresh):
    results = []
    for lr, lt in rt_lines:
        found = False
        for rr, rt, sim_lines in results:
            dr = np.abs(rr-lr)
            dt = np.abs(rt-lt)
            if dr < r_thresh and dt < theta_thresh:
                found = True
                sim_lines.append((lr, lt))
                break
        if not found:
            results.append((lr, lt, [(lr, lt)]))
    deduped = []
    for r, t, sim_lines in results:
        r_sum = 0
        t_sum = 0
        lc = len(sim_lines)
        for lr, lt in sim_lines:
            r_sum += lr
            t_sum += lt
        deduped.append((r_sum/lc, t_sum/lc))
    return deduped

def rt_lines_to_2pts(rt_lines):
    two_pts_lines = []
    for rho, theta in rt_lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        two_pts_lines.append([x1, y1, x2, y2])
    return two_pts_lines


# threshold = slope threshold
def orthogonal_separation(lines, threshold=10):
    horizontal = []
    vertical = []
    for x1, y1, x2, y2 in lines:
        dx = np.abs(x1-x2)
        dy = np.abs(y1-y2)
        if dx == 0 and dy == 0:
            # incorrect line
            continue
        if dy == 0 or dx/dy > threshold:
            horizontal.append([x1,y1,x2,y2])
        elif dx == 0 or dy/dx > threshold:
            vertical.append([x1,y1,x2,y2])
        # else noise
    return horizontal, vertical


def sort_2pts_lines(lines, index):
    lines.sort(cmp=lambda l1, l2: l1[index] - l2[index])

def find_two_lines_intersection(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    d = ((x1-x2) * (y3-y4)) - ((y1-y2) * (x3-x4))
    if d != 0:
        px = int(((x1*y2 - y1*x2) * (x3-x4) - (x1-x2) * (x3*y4 - y3*x4)) / d)
        py = int(((x1*y2 - y1*x2) * (y3-y4) - (y1-y2) * (x3*y4 - y3*x4)) / d)
        return px, py
    else:
        return None


# def find_intersections(lines1, lines2):
#     vertices = []
#     for line1 in lines1:
#         for line2 in lines2:
#             intersect = find_two_lines_intersection(line1, line2)
#             if intersect is not None:
#                 vertices.append(intersect)
#     return vertices


def eudist(p1, p2):
    p1x, p1y = p1
    p2x, p2y = p2
    dx = p1x-p2x
    dy = p1y-p2y
    return np.sqrt(dx*dx+dy*dy)


def find_nearest_point(vert, verts):
    if len(verts) == 0:
        return -1, None
    return min([(eudist(vert, v), v) for v in verts])


# lines1 and lines2 must be sorted. thresh: max difference to consider same vertex
def find_intersection_matrix(horizontals, verticals, thresh=0):
    verts = []
    mat = []
    for l1 in horizontals:
        row = []
        for l2 in verticals:
            vert = find_two_lines_intersection(l1, l2)
            dist, v = find_nearest_point(vert, verts)
            if v is None or dist > thresh:
                row.append(vert)
                verts.append(vert)
        if len(row) > 0:
            mat.append(row)
    return mat, verts


# slide_fn(top-left, top-right, bottom-left, bottom-right, is_new_row)
def slide_vertex_mat_4pts(v_mat, slide_fn):
    for i in range(0, len(v_mat)-1):
        is_new_row = True
        top_row = v_mat[i]
        bot_row = v_mat[i+1]
        if len(top_row) != len(bot_row):
            # bug?
            continue
        for j in range(0, len(top_row)-1):
            tl = top_row[j]
            tr = top_row[j+1]
            bl = bot_row[j]
            br = bot_row[j+1]
            slide_fn(tl, tr, bl, br, is_new_row)
            is_new_row = False


# def deduplicate_vertices(vertices, threshold):
#     results = []
#     for vx, vy in vertices:
#         found = False
#         for rx, ry in results:
#             dx = vx-rx
#             dy = vy-ry
#             eudiff = np.sqrt(dx*dx+dy*dy)
#             if eudiff < threshold:
#                 found = True
#                 break
#         if not found:
#             results.append((vx, vy))
#     return results


# def create_vertex_matrix(vertices, y_thresh):
#     results = []
#     for vx, vy in vertices:
#         found = False
#         for r in results:
#             r1x, r1y = r[0]
#             dy = np.abs(vy - r1y)
#             if dy < y_thresh:
#                 r.append((vx, vy))
#                 found = True
#                 break
#         if not found:
#             results.append([(vx, vy)])
#
#     results.sort(cmp=lambda r1, r2: r1[0][1] - r2[0][1])
#     return results