"""
utils for collision check
@author: huiming zhou
"""

import math
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                "/../../Sampling_based_Planning/")

from Sampling_based_Planning.rrt_2D import envRCAR
from Sampling_based_Planning.rrt_2D.rrt import Node


class Utils:
    def __init__(self):
        self.env = envRCAR.Env()

        self.delta = 150
        self.obs_circle = self.env.obs_circle
        self.obs_rectangle = self.env.obs_rectangle
        self.obs_boundary = self.env.obs_boundary

    def update_obs(self, obs_cir, obs_bound, obs_rec):
        self.obs_circle = obs_cir
        self.obs_boundary = obs_bound
        self.obs_rectangle = obs_rec

    def get_obs_vertex(self):
        delta = self.delta
        obs_list = []

        for (ox, oy, w, h) in self.obs_rectangle:
            vertex_list = [[ox , oy ],
                           [ox + w , oy ],
                           [ox + w , oy + h ],
                           [ox , oy + h ]]
            obs_list.append(vertex_list)

        return obs_list

    def is_intersect_rec(self, start, end, o, d, a, b): #让路径中的任意两点不碰到矩形障碍物
        v1 = [o[0] - a[0], o[1] - a[1]]
        v2 = [b[0] - a[0], b[1] - a[1]]
        v3 = [-d[1], d[0]]

        div = np.dot(v2, v3)

        if div == 0:
            return False

        t1 = np.linalg.norm(np.cross(v2, v1)) / div
        t2 = np.dot(v1, v3) / div

        if t1 >= 0 and 0 <= t2 <= 1:
            shot = Node((o[0] + t1 * d[0], o[1] + t1 * d[1]))
            dist_obs = self.get_dist(start, shot)
            dist_seg = self.get_dist(start, end)
            if dist_obs <= dist_seg:
                return True

        return False

    def is_intersect_circle(self, o, d, a, r):  #让路径中的任意两点不碰到圆形障碍物
        d2 = np.dot(d, d)
        delta = self.delta

        if d2 == 0:
            return False

        t = np.dot([a[0] - o[0], a[1] - o[1]], d) / d2

        if 0 <= t <= 1:
            shot = Node((o[0] + t * d[0], o[1] + t * d[1]))
            if self.get_dist(shot, Node(a)) <= r + delta:
                return True

        return False

    def is_collision(self, start, end):
        if self.is_inside_obs(start) or self.is_inside_obs(end):
            return True

        o, d = self.get_ray(start, end)
        obs_vertex = self.get_obs_vertex()

        for (v1, v2, v3, v4) in obs_vertex:
            if self.is_intersect_rec(start, end, o, d, v1, v2):
                return True
            if self.is_intersect_rec(start, end, o, d, v2, v3):
                return True
            if self.is_intersect_rec(start, end, o, d, v3, v4):
                return True
            if self.is_intersect_rec(start, end, o, d, v4, v1):
                return True

        for (x, y, r) in self.obs_circle:
            if self.is_intersect_circle(o, d, [x, y], r):
                return True

        return False

    def is_inside_obs(self, node):
        delta = self.delta

        for (x, y, r) in self.obs_circle:
            if math.hypot(node.x - x, node.y - y) <= r + delta:
                return True

        for (x, y, w, h) in self.obs_rectangle:  #矩形碰撞
            minx = min(abs(x - node.x), abs(x+w - node.x))
            miny = min(abs(y - node.y), abs(y+h- node.y))
            if (minx * minx + miny * miny < delta * delta):
                return True
            x0 = (x + x+w) / 2
            y0 = (y + y+h) / 2
            if ((abs(x0 - node.x) < abs(w) / 2 + delta) and abs(node.y - y0) < abs(h) / 2):
                return True
            if ((abs(y0 - node.y) < abs(h) / 2 + delta)and abs(node.x - x0) < abs(w) / 2):
                return True


            # if 0 <= node.x - (x - delta) <= w + 2 * delta \
            #         and 0 <= node.y - (y - delta) <=h + 2 * delta:
            #     return True

        for (x, y, w, h) in self.obs_boundary:   #矩形碰撞
            if 0 <= node.x - (x - delta) <= w  + 2 * delta \
                    and 0 <= node.y - (y - delta) <= h + 2 * delta:
                return True

        return False

    @staticmethod
    def get_ray(start, end):
        orig = [start.x, start.y]
        direc = [end.x - start.x, end.y - start.y]
        return orig, direc

    @staticmethod
    def get_dist(start, end):
        return math.hypot(end.x - start.x, end.y - start.y)  #math.hypot为求范数