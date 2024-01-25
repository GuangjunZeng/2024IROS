"""
Fast Marching Trees (FMT*)
@author: huiming zhou
"""
#from fenics import *

import os
import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd


sys.path.append("C:\\Users\\admin\\Desktop\\ICRA-2024-Yuezhen Liu\\Sampling_based_Planning")

from Sampling_based_Planning.rrt_2D import envRCAR, plotting, utils


class Node:
    def __init__(self, n):
        self.x = n[0]
        self.y = n[1]
        self.parent = None
        self.cost = np.inf


class FMT:
    def __init__(self, x_start, x_goal, search_radius):  #最后一个是搜索半径？
        self.x_init = Node(x_start)
        self.x_goal = Node(x_goal)
        self.search_radius = search_radius

        self.env = envRCAR.Env()
        self.plotting = plotting.Plotting(x_start, x_goal)
        self.utils = utils.Utils()

        self.fig, self.ax = plt.subplots()
        self.delta = self.utils.delta
        self.x_range = self.env.x_range
        self.y_range = self.env.y_range
        self.obs_circle = self.env.obs_circle
        self.obs_rectangle = self.env.obs_rectangle
        self.obs_boundary = self.env.obs_boundary

        self.V = set()
        self.V_unvisited = set()
        self.V_open = set()
        self.V_closed = set()
        self.sample_numbers = 2000  #采样时间

    def Init(self):
        samples = self.SampleFree()

        self.x_init.cost = 0.0
        self.V.add(self.x_init)
        self.V.update(samples)
        self.V_unvisited.update(samples)
        self.V_unvisited.add(self.x_goal)
        self.V_open.add(self.x_init)

    def Planning(self):
        self.Init()
        z = self.x_init
        n = self.sample_numbers
        rn = self.search_radius * math.sqrt((math.log(n) / n))
        Visited = []

        while z is not self.x_goal:
            V_open_new = set()
            X_near = self.Near(self.V_unvisited, z, rn)
            Visited.append(z)

            for x in X_near:
                Y_near = self.Near(self.V_open, x, rn)
                cost_list = {y: y.cost + self.Cost(y, x) for y in Y_near}
                y_min = min(cost_list, key=cost_list.get)

                if not self.utils.is_collision(y_min, x):
                    x.parent = y_min
                    V_open_new.add(x)
                    self.V_unvisited.remove(x)
                    x.cost = y_min.cost + self.Cost(y_min, x)

            self.V_open.update(V_open_new)
            self.V_open.remove(z)
            self.V_closed.add(z)

            if not self.V_open:
                print("open set empty!")
                break

            cost_open = {y: y.cost for y in self.V_open}
            z = min(cost_open, key=cost_open.get)

        # node_end = self.ChooseGoalPoint()
        path_x, path_y = self.ExtractPath()
        self.animation(path_x, path_y, Visited[1: len(Visited)])

    def ChooseGoalPoint(self):
        Near = self.Near(self.V, self.x_goal, 2.0)
        cost = {y: y.cost + self.Cost(y, self.x_goal) for y in Near}

        return min(cost, key=cost.get)

    def ExtractPath(self):
        path_x, path_y = [], []
        node = self.x_goal

        while node.parent:
            path_x.append(node.x)
            path_y.append(node.y)
            node = node.parent

        path_x.append(self.x_init.x)
        path_y.append(self.x_init.y)

        return path_x, path_y

    def Cost(self, x_start, x_end):
        if self.utils.is_collision(x_start, x_end):
            return np.inf
        else:
            return self.calc_dist(x_start, x_end)

    @staticmethod
    def calc_dist(x_start, x_end):
        return math.hypot(x_start.x - x_end.x, x_start.y - x_end.y)

    @staticmethod
    def Near(nodelist, z, rn):
        return {nd for nd in nodelist
                if 0 < (nd.x - z.x) ** 2 + (nd.y - z.y) ** 2 <= rn ** 2}

    def SampleFree(self):
        n = self.sample_numbers
        delta = self.utils.delta
        Sample = set()

        ind = 0
        while ind < n:
            node = Node((random.uniform(self.x_range[0] + delta, self.x_range[1] - delta),
                         random.uniform(self.y_range[0] + delta, self.y_range[1] - delta)))
            if self.utils.is_inside_obs(node):
                continue
            else:
                Sample.add(node)
                ind += 1

        return Sample

    def animation(self, path_x, path_y, visited):
        self.plot_grid("Fast Marching Trees (FMT*)")

        for node in self.V:
            plt.plot(node.x, node.y, marker='.', color='white', markersize=3)

        count = 0



        for node in visited:
            count += 1
            plt.plot([node.x, node.parent.x], [node.y, node.parent.y], '-g')
            plt.gcf().canvas.mpl_connect(
                'key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None])
            if count % 10 == 0:
                plt.pause(0.001)

        plt.plot(path_x, path_y, linewidth=2, color='red')
        afile = open("C:\\Users\\admin\Desktop\\ICRA-2024-Yuezhen Liu\\Sampling_based_Planning\callx3.txt", "a")
        afile.write(str(path_x))
        afile.write("\n")
        afile.close()
        afile = open("C:\\Users\\admin\Desktop\\ICRA-2024-Yuezhen Liu\\Sampling_based_Planning\cally3.txt", "a")
        afile.write(str(path_y))
        afile.write("\n")
        afile.close()
        print([path_x,path_y])
        plt.pause(0.01)
        plt.show()

        # 将数据转换为pandas DataFrame
        df = pd.DataFrame({'path_x': path_x, 'path_y': path_y})

        # 检查是否存在文件并追加或写入数据
        output_file = "C:\\Users\\admin\\Desktop\\ICRA-2024-Yuezhen Liu\\Sampling_based_Planning\\data.xlsx"

        try:
            with pd.ExcelWriter(output_file, engine='openpyxl', mode='a') as writer:
                # 如果文件存在并具有数据
                existing_data = pd.read_excel(output_file)
                df_to_write = pd.concat([existing_data, df], ignore_index=True)
                df_to_write.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
        except FileNotFoundError:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)


    def plot_grid(self, name):

        for (ox, oy, w, h) in self.obs_boundary:
            self.ax.add_patch(
                patches.Rectangle(
                    (ox, oy), w, h,
                    edgecolor='black',
                    facecolor='black',
                    fill=True
                )
            )

        for (ox, oy, w, h) in self.obs_rectangle:
            self.ax.add_patch(
                patches.Rectangle(
                    (ox, oy), w, h,
                    edgecolor='black',
                    facecolor='black',
                    fill=True
                )
            )

        for (ox, oy, r) in self.obs_circle:
            self.ax.add_patch(
                patches.Circle(
                    (ox, oy), r,
                    edgecolor='black',
                    facecolor='gray',
                    fill=True
                )
            )



        plt.plot(self.x_init.x, self.x_init.y, "bs", linewidth=3)
        plt.plot(self.x_goal.x, self.x_goal.y, "rs", linewidth=3)

        plt.title(name)
        plt.axis("equal")


def main():
    x_start = (350, 350)  # Starting node [150,1900]
    x_goal = (1450, 1400)  # Goal node [1475,685]


    fmt = FMT(x_start, x_goal, 1000)
    fmt.Planning()


if __name__ == '__main__':
    main()