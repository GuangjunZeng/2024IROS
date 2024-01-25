"""
Environment for rrt_2D
@author: huiming zhou
"""


class Env:
    def __init__(self):
        self.x_range = (0, 2048)
        self.y_range = (0, 2048)
        self.obs_boundary = self.obs_boundary()
        self.obs_circle = self.obs_circle()
        self.obs_rectangle = self.obs_rectangle()

    @staticmethod
    def obs_boundary():
        obs_boundary = [


        ]
        return obs_boundary

    @staticmethod
    def obs_rectangle():
        obs_rectangle = [#左上角点横坐标，左上角点纵坐标，长，宽
            [0, 0, 40, 2048], #前四个是四条边
            [0, 0, 2048, 40],
            [2008, 0, 40, 2048],
            [0, 2008, 2048, 40],

            [800, 1100, 450, 170],  ##left top right bottom: 800
            [240, 850, 130, 130],
            [580, 400, 150, 150]
        ]
        return obs_rectangle

    @staticmethod
    def obs_circle():
        obs_cir = [
           [520,1550,130],  # 中心点坐标,半径
           [1100,520,130],
           [1600,680,150]
        ]

        return obs_cir